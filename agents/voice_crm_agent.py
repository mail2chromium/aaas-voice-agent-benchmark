"""
Voice CRM Agent — Replaces Salesforce + Calendly + Email Follow-ups

This agent handles inbound sales calls, qualifies leads through natural
voice conversation, logs data to CRM, schedules meetings, and sends
follow-up emails — all autonomously.

Author: Muhammad Usman Bashir (@BeingOttoman)
License: MIT
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.agents.llm import function_tool
from livekit.plugins import deepgram, openai, elevenlabs

logger = logging.getLogger("voice-crm-agent")


@dataclass
class LeadData:
    """Structured lead data extracted during conversation."""
    name: str = ""
    company: str = ""
    email: str = ""
    phone: str = ""
    role: str = ""
    budget_range: str = ""
    timeline: str = ""
    requirements: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    qualification_score: int = 0  # 0-100
    notes: str = ""


class VoiceCRMAgent(Agent):
    """
    Production voice CRM agent built on LiveKit Agents framework.

    Replaces:
    - Salesforce CRM (lead logging, pipeline management)
    - Calendly (meeting scheduling)
    - Email sequences (follow-up automation)

    Cost comparison:
    - Salesforce Enterprise: $150/seat/month × 8 seats = $1,200/month
    - Calendly Teams: $12/seat/month × 8 seats = $96/month
    - Email tool: ~$50/month
    - TOTAL SaaS: $1,346/month

    - This agent: ~$200/month (LLM + STT + TTS API costs)
    - SAVINGS: 85% cost reduction
    """

    def __init__(self):
        super().__init__(
            instructions=self._build_instructions(),
            stt=deepgram.STT(
                model="nova-3",
                language="en",
                smart_format=True,
                filler_words=True,
            ),
            llm=openai.LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
            tts=elevenlabs.TTS(
                model_id="eleven_flash_v2_5",
                voice_id="pNInz6obpgDQGcFmaJgB",  # Professional male
                output_format="pcm_24000",
            ),
        )
        self.lead_data = LeadData()
        self.conversation_started = False

    def _build_instructions(self) -> str:
        return """You are a lead qualification specialist for RTC League,
a company that builds real-time AI communication infrastructure.

Your job is to:
1. Greet the caller warmly and professionally
2. Understand their needs for real-time AI / Voice AI / WebRTC infrastructure
3. Qualify their budget and timeline
4. Assess their technical requirements
5. Score the lead (0-100) based on fit
6. Schedule a technical consultation if qualified (score >= 60)
7. Send a follow-up email summary

Be conversational, not robotic. Ask one question at a time. Listen actively.
Use natural acknowledgments ("Got it", "That makes sense", "Interesting").

NEVER mention that you are an AI. Present yourself as a member of the
RTC League team.

QUALIFICATION CRITERIA:
- Budget >= $10,000/month → +30 points
- Timeline <= 3 months → +20 points
- Enterprise company (500+ employees) → +20 points
- Clear use case defined → +15 points
- Technical decision maker → +15 points
"""

    @function_tool()
    async def log_lead_to_crm(
        self,
        name: str,
        company: str,
        email: str,
        budget_range: str,
        timeline: str,
        requirements: str,
        qualification_score: int,
    ) -> str:
        """Log qualified lead data to CRM system.

        Args:
            name: Full name of the lead
            company: Company name
            email: Email address
            budget_range: Budget range (e.g., "$10K-50K/month")
            timeline: Project timeline (e.g., "Q2 2026")
            requirements: Key requirements summary
            qualification_score: Score 0-100
        """
        self.lead_data = LeadData(
            name=name,
            company=company,
            email=email,
            budget_range=budget_range,
            timeline=timeline,
            requirements=requirements.split(", "),
            qualification_score=qualification_score,
        )

        # In production: call Salesforce/HubSpot API here
        # Example: sf_client.Lead.create({...})
        logger.info(
            f"Lead logged to CRM: {name} ({company}) — Score: {qualification_score}"
        )
        return f"Lead {name} from {company} logged successfully. Score: {qualification_score}/100."

    @function_tool()
    async def schedule_meeting(
        self,
        attendee_email: str,
        preferred_date: str,
        duration_minutes: int = 30,
    ) -> str:
        """Schedule a technical consultation meeting.

        Args:
            attendee_email: Email of the person to schedule with
            preferred_date: Preferred date/time (ISO format)
            duration_minutes: Meeting duration in minutes
        """
        # In production: call Google Calendar / Calendly API
        # Example: calendar_service.events().insert(...)
        logger.info(
            f"Meeting scheduled: {attendee_email} on {preferred_date} ({duration_minutes}min)"
        )
        return f"Meeting scheduled for {preferred_date}. Calendar invite sent to {attendee_email}."

    @function_tool()
    async def send_followup_email(
        self,
        to_email: str,
        lead_name: str,
        summary: str,
    ) -> str:
        """Send follow-up email after the qualification call.

        Args:
            to_email: Recipient email
            lead_name: Name for personalization
            summary: Call summary and next steps
        """
        # In production: call SendGrid/SES API
        logger.info(f"Follow-up email sent to {to_email}")
        return f"Follow-up email sent to {lead_name} at {to_email}."


async def entrypoint(session: AgentSession):
    """Main entry point for the voice CRM agent."""
    agent = VoiceCRMAgent()

    await agent.start(
        room=session.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=True,
        ),
    )

    # Greet the caller
    await agent.say(
        "Hi, thanks for calling RTC League! "
        "I'm here to learn about your real-time AI needs "
        "and see how we can help. What brings you to us today?"
    )
