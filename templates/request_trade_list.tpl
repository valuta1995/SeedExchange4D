<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">
    <property name="inputmodes" value="dtmf"/>
    <form id="request_trade_list">
        <field name="form_trade_id" type="number">
            <prompt>
                <p>
                    <s>There are {{len(trade_list)}} offers that match your search.</s>
                    <s>Please enter the number of the listing you wish to listen to.</s>
                </p>
            </prompt>
            <filled>
                <assign name="trade_id" expr="form_trade_id"/>
            </filled>
        </field>

        <filled>
            <goto nextexpr="'/trades/' + trade_id"/>
        </filled>
    </form>
</vxml>