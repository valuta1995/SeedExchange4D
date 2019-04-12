<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>

    <menu id="main_menu" scope="dialog">
        <prompt>
            Welcome
        </prompt>

        <prompt>
            <break time="500"/>
            To provide seeds in trade, press 1.
            To request seeds in trade, press 2.
            To check on your current trades, press 3.
        </prompt>

        <choice next="#provide_trade" dtmf="1"/>
        <choice next="#request_trade" dtmf="2"/>
        <choice next="#check_trade" dtmf="3"/>
    </menu>

    <form id="provide_trade">
        <block>
            <assign name="provide_unit" expr="'bags'"/>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <submit next="/provide_trade.vxml#stage_1" namelist="caller_id provide_unit"/>
        </block>
    </form>

    <form id="request_trade">
        <block>
            <assign name="provide_unit" expr="'bags'"/>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <submit next="/request_trade.vxml#stage_1" namelist="caller_id provide_unit"/>
        </block>
    </form>

    <form id="check_trade">
        <block>
            <assign name="provide_unit" expr="'bags'"/>
            <assign name="caller_id" expr="session.connection.remote.uri"/>
            <submit next="/check_trade.vxml#stage_1" namelist="caller_id provide_unit"/>
        </block>
    </form>

    <form id="leave">
        <block>
            <prompt>
                <p>
                    <s>We wish you a good day!</s>
                </p>
            </prompt>
        </block>
        <disconnect/>
    </form>
</vxml>