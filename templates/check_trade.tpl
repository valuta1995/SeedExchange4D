<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>


    <!-- At this stage the user tells the system what seeds they have available -->
    <menu id="stage_1">
        <prompt>
            <p>
                <s>What seeds do you want to offer?</s>
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
        <choice next="/main_menu.vxml#main_menu" dtmf="0"/>
    </menu>

</vxml>