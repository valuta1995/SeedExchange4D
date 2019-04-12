<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">
    <property name="inputmodes" value="dtmf"/>
    <form id="contact">
        <block>
            <prompt>
                <p>
                    <s>Offer deleted.</s>
                </p>
            </prompt>
            <submit next="/check_trade.vxml#stage_1" namelist="caller_id"/>
        </block>
    </form>
</vxml>