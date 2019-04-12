<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>

    <!-- handle event for storing offer and moving to request -->
    <catch event="on_provide_selected">
        <prompt>.</prompt>

        <assign name="provide_name" expr="_message"/>
        <assign name="provide_unit" expr="'bags'"/>

        <goto next="#stage_2"/>
    </catch>

    <!-- handle event for storing request and moving to info -->
    <catch event="on_request_selected">
        <prompt>.</prompt>

        <assign name="request_name" expr="_message"/>
        <assign name="request_unit" expr="'bags'"/>

        <goto next="#stage_3"/>
    </catch>

    <!-- handle event for storing request and moving to info -->
    <catch event="on_transport_selected">
        <prompt>.</prompt>

        <assign name="transport_name" expr="_message"/>
        <if cond="_message == 'deliver'">
            <assign name="transport_desciption" expr="you will deliver to the other person"/>
        </if>

        <if cond="_message == 'pick up'">
            <assign name="transport_desciption" expr="the other person will have to pick up"/>
        </if>

        <goto next="#stage_4"/>
    </catch>

    <!-- TODO make this part actually do things ! -->
    <catch event="on_provide_selected_other on_request_selected_other on_transport_selected_other">
        <prompt>This functionality is not yet available.</prompt>
        <disconnect/>
    </catch>

    <!-- At this stage the user tells the system what seeds they have available -->
    <menu id="stage_1">
        <prompt>
            <p>
                <s>What seeds do you have?</s>
            </p>
            <break time="500"/>
            <p>
                % for i in range(0, len(seed_list)):
                <s>To offer {{seed_list[i]['name']}}, press {{i + 1}}</s>
                % end

                <s>To offer something else, press 9.</s>
                <s>To go back, press 0.</s>
            </p>
        </prompt>

        % for i in range(0, len(seed_list)):
        <choice event="on_provide_selected" message="{{seed_list[i]['name']}}" dtmf="{{i + 1}}"/>
        % end

        <choice event="on_provide_selected_other" message="other" dtmf="9"/>
        <choice next="main_menu.vxml#main_menu" dtmf="0"/>
    </menu>

    <!-- At this stage the user tells the system what seeds they want -->
    <menu id="stage_2">
        <prompt>
            <p>
                <s>
                    You have offered to trade
                    <value expr="provide_unit"/>
                    of
                    <value expr="provide_name"/>
                    away.
                </s>
            </p>
            <p>
                <s>What seeds are you looking for?</s>
            </p>
            <break time="500"/>
            <p>
                % for i in range(0, len(seed_list)):
                <s>To request {{seed_list[i]['name']}}, press {{i + 1}}</s>
                % end

                <s>To request something else, press 9.</s>
                <s>To go back, press 0.</s>
            </p>
        </prompt>

        % for i in range(0, len(seed_list)):
        <choice event="on_request_selected" message="{{seed_list[i]['name']}}" dtmf="{{i + 1}}"/>
        % end

        <choice event="on_request_selected_other" message="other" dtmf="9"/>
        <choice next="#stage_1" dtmf="0"/>
    </menu>

    <!-- At this stage the user tells the system if they have transportation available -->
    <menu id="stage_3">
        <prompt>
            <p>
                <s>
                    You want to receive
                    <value expr="request_unit"/>
                    of
                    <value expr="request_name"/>
                    .
                </s>
            </p>
            <p>
                <s>Can you transport the seeds to the other person or will they have to come to pick them up?</s>
            </p>
            <break time="500"/>
            <p>
                <s>If you can deliver, press 1.</s>
                <s>If you want a pick up, press 2.</s>

                <s>To organise something else, press 9.</s>
                <s>To go back, press 0.</s>
            </p>
        </prompt>

        <choice event="on_transport_selected" message="deliver" dtmf="1"/>
        <choice event="on_transport_selected" message="pick up" dtmf="2"/>

        <choice event="on_transport_selected_other" message="" dtmf="9"/>
        <choice next="#stage_2" dtmf="0"/>
    </menu>

    <!-- At this stage we verify with the user that all is ok -->
    <menu id="stage_4">
        <prompt>
            <p>
                <s>
                    You have
                    <value expr="provide_unit"/>
                    of
                    <value expr="provide_name"/>
                    available.
                </s>
                <s>
                    You want to receive
                    <value expr="request_unit"/>
                    of
                    <value expr="request_name"/>
                    .
                </s>
                <s>
                    You have indicated that
                    <value expr="transport_description"/>
                    .
                </s>
            </p>
            <p>
                <s>If this is correct, press 1.</s>
                <s>If this is not correct, press 2.</s>
            </p>
        </prompt>

        <choice next="#stage_5" dtmf="1"/>
        <choice next="#stage_1" dtmf="2"/>
    </menu>


    <block id="stage_5">
        <submit next="search_trade" namelist="provide_name provide_unit request_name request_unit transport_name"/>
    </block>


    <!-- At this stage the user is asked if they want to exit or go again -->
    <menu id="stage_finished" scope="dialog" dtmf="true">
        <prompt>
            <p>
                <s>Your offer has been recorded.</s>
                <s>To make another offer, press 1.</s>
                <s>To go to the main menu, press 2.</s>
                <s>If you are finished, press 3.</s>
            </p>
        </prompt>
        <choice next="#stage_1" dtmf="1"/>
        <choice next="main_menu.vxml#main_menu" dtmf="2"/>
        <choice next="main_menu.vxml#disconnect" dtmf="3"/>
    </menu>
</vxml>