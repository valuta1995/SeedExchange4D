<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">
    <property name="inputmodes" value="dtmf"/>
    <menu id="stage_1">
        <prompt>
            <p>
                <s>
                    This is the offer of
                    <audio expr="{{trade_entry.audio}}"/>
                </s>
                <s>
                    They offer {{trade_entry.provide_unit}} of {{trade_entry.provide_name}} for your
                    {{trade_entry.request_unit}} of {{trade_entry.request_name}}.
                </s>
            </p>
            <p>
                <s>If you want to contact this person, press 1.</s>
                <s>If you want to listen to another offer, press 2.</s>
            </p>
        </prompt>

        <choice next="#contact" dtmf="1"/>
        <choice next="#return" dtmf="2"/>
    </menu>

    <form id="return">
        <block>
            <submit next="search_trade" method="post"
                    namelist="provide_name provide_unit request_name request_unit transport_name"/>
        </block>
    </form>

    <form id="contact">
        <block>
            <prompt>
                <p>
                    <s>This functionality is not yet implemented.</s>
                    <s>The current idea is that the system will attempt a transfer to the poster of the offer.</s>
                    <s>The poster can then decide whether or not to accept the call.</s>
                    <s>The poster will also have the option to mark the offer as already finished.</s>
                </p>
            </prompt>
            <goto next="/main_menu.vxml#leave"/>
        </block>
    </form>
</vxml>