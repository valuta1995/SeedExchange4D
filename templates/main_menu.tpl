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

        <choice next="provide_trade.vxml#stage_1" dtmf="1"/>
        <choice next="request_trade.vxml#stage_1" dtmf="2"/>
        <choice next="check_trade.vxml#stage_1" dtmf="3"/>
    </menu>

    <form id="leave">
        <prompt>
            <p>
                <s>We wish you a good day!</s>
            </p>
        </prompt>
        <disconnect/>
    </form>
</vxml>