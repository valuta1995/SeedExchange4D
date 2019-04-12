<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">
    <property name="inputmodes" value="dtmf"/>
    <form id="stage_1">
        <field name="form_id" type="number">
            <prompt>
                <p>
                    <s>
                        There are
                        <value expr="{{len(trade_list)}}"/>
                        offers that match your search.
                    </s>
                    <s>Please enter the number of the listing you wish to listen to.</s>
                </p>
            </prompt>
            <filled>
                <goto nextexpr="'/trades/' + form_id"/>
            </filled>
        </field>
    </form>
</vxml>