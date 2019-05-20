<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>

    <menu id="main_menu" scope="dialog">
        <prompt>
            <audio src="/static/en/welcome.wav"/>
            <break time="500"/>
            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/making-a-trade-offer.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/1.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/listening-to-existing-trade-offers.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/2.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/managing-your-current-offers.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/3.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/done-with-system.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/0.wav"/>
        </prompt>

        <choice next="#provide_trade" dtmf="1"/>
        <choice next="#request_trade" dtmf="2"/>
        <choice next="#check_trade" dtmf="3"/>
        <choice next="#leave" dtmf="0"/>
    </menu>

    <form id="provide_trade">
        <block>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <assign name="caller_mode" expr="'provide_trade'"/>
            <submit next="/provide_trade.vxml#stage_1" namelist="caller_id"/>
        </block>
    </form>

    <form id="request_trade">
        <block>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <assign name="caller_mode" expr="'request_trade'"/>
            <submit next="/request_trade.vxml#stage_1" namelist="caller_id"/>
        </block>
    </form>

    <form id="check_trade">
        <block>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <assign name="caller_mode" expr="'check_trade'"/>
            <submit next="/check_trade.vxml#stage_1" namelist="caller_id"/>
        </block>
    </form>

    <form id="leave">
        <block>
            <prompt>
                <audio src="/static/en/thank-you-good-day.wav"/>
                <break time="500"/>
            </prompt>
        </block>
        <disconnect/>
    </form>
</vxml>