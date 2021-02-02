# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import ChannelAccount


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    IN_CHANNEL = [] #TeamsInfo.get_members() # I actually cant use this because I have to give a turn context to it...
    REPORTED = []
    DID_NOT_REPORT = []
    RED = []
    AMBER = []
    GREEN = []


    async def on_message_activity(self, turn_context: TurnContext):
        print("[+] In on_message")
        IN_CHANNEL = await TeamsInfo.get_members(turn_context)

        text = turn_context.activity.text.strip().lower()
        print("[+] User message: " + text)

        member = await self._get_member(turn_context)
        print("[+] This is who sent the message")
        if "red" in text:
            print("[-] Oh shiddd, someone got the rona, appending you to the red list")
            RED.append(member)
        
        if "amber" in text or "yellow" in text:
            print("[-] You're probably fine but *playing it safe*, yeah, okay. Added to AMBER list")
            RED.append(member)

        if "green" in text:
            print("[+] Cool, see you at work! Adding to to green list")
            RED.append(member)

        await turn_context.send_activity("Got your status, thank you!")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def _get_member(self, turn_context: TurnContext):
        print("[+] In get_member")
        TeamsChannelAccount: member = None
        try:
            member = await TeamsInfo.get_member(
                turn_context, turn_context.activity.from_property.id
            )
        except Exception as e:
            if "MemberNotFoundInConversation" in e.args[0]:
                await turn_context.send_activity("Member not found.")
            else:
                raise
        else:
            return member.name
            #await turn_context.send_activity(f"You are: {member.name}")

# Things to do
# Find a way to get all the users in a channel into a python list
# Create the logic to take them out of that list and put them into a different one