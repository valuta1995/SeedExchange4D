<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>

    <catch event="listen_to_entry">
        % for i in range(len(trade_list)):
        <if cond="_message == {{i + 1}}">
            <goto next="/trades/{{trade_list[i]['id']}}.vxml"/>
        </if>
        % end
        <goto next="#invalid"/>
    </catch>

    <catch event="delete_entry">
        % for i in range(len(trade_list)):
        <if cond="_message == {{i + 1}}">
            <submit next="/trades/delete/{{trade_list[i]['id']}}.vxml" namelist="caller_id"/>
        </if>
        % end
        <goto next="#invalid"/>
    </catch>

    <!-- At this stage the user tells the system what seeds they have available -->
    <form id="stage_1">
        <field name="form_trade_id" type="number">
            <prompt>
                <p>
                    <s>You have {{len(user_data['trade_list'])}} offers posted.</s>
                    <s>Please enter the number of the listing you wish to listen to.</s>
                </p>
            </prompt>
            <filled>
                <assign name="trade_id" expr="form_trade_id"/>
            </filled>
        </field>
        <filled>
            <goto next="#manage_entry"/>
        </filled>
    </form>

    <menu id="manage_entry">
        <prompt>
            <p>
                <s>If you wish to listen to your offer, press 1.</s>
                <s>If you wish to delete your offer, press 2.</s>
            </p>
        </prompt>

        <choice event="listen_to_entry" messageexpr="trade_id" dtmf="1"/>
        <choice event="delete_entry" messageexpr="trade_id" dtmf="2"/>
    </menu>

    <form id="invalid">
        <block>
            <p>
                <s>There are only {{len(trade_list)}} entries.</s>
                <s>Please select a different entry.</s>
            </p>
        </block>
        <goto next="#stage_1"/>
    </form>
</vxml>