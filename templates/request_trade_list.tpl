<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">
    <property name="inputmodes" value="dtmf"/>
    <form id="request_trade_list">
        <field name="form_trade_id" type="number">
            <prompt>
                <p>
                    <s>There are {{len(trade_list)}} offers that match your search.</s>
                    <s>
                        Please enter the number of the listing you wish to listen to,
                        or enter 0 to return to the start.
                    </s>
                </p>
            </prompt>
            <filled>
                <assign name="trade_id" expr="form_trade_id"/>
            </filled>
        </field>

        <filled>
            <if cond="trade_id == 0">
                <goto next="/main_menu.vxml#main_menu"/>
            </if>
            % for i in range(len(trade_list)):
            <if cond="trade_id == {{i + 1}}">
                <goto next="/trades/{{trade_list[i]['id']}}.vxml"/>
            </if>
            % end
            <goto next="#invalid"/>
        </filled>
    </form>

    <form id="invalid">
        <block>
            <p>
                <s>There are only {{len(trade_list)}} entries.</s>
                <s>Please select a different entry.</s>
            </p>
        </block>
        <goto next="#request_trade_list"/>
    </form>
</vxml>