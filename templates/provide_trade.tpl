<?xml version="1.0" encoding="UTF-8"?>
<vxml version="{{vxml_version}}" application="{{application}}">

    <!-- set input to DTMF-->
    <property name="inputmodes" value="dtmf"/>

    <!-- handle event for storing offer and moving to request -->
    <catch event="on_provide_selected">
        <assign name="provide_name" expr="_message"/>
        <!--<assign name="provide_unit" expr="'bags'"/>-->

        <goto next="#stage_2"/>
    </catch>

    <!-- handle event for storing request and moving to info -->
    <catch event="on_request_selected">
        <assign name="request_name" expr="_message"/>
        <!--<assign name="request_unit" expr="'bags'"/>-->

        <!--<goto next="#stage_3"/>-->
        <!-- Going directly to stage 4, skipping transport -->
        <goto next="#stage_4"/>
    </catch>

    <!-- handle event for storing request and moving to info -->
    <catch event="on_transport_selected">

        <assign name="transport_name" expr="_message"/>
        <assign name="transport_description" expr="'you and the other person will figure out another way'"/>

        <if cond="_message == 'true'">
            <assign name="transport_description" expr="'you can transport if need be'"/>
        </if>

        <if cond="_message == 'false'">
            <assign name="transport_description" expr="'you cannot transport.'"/>
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
            <audio src="/static/en/you-have-chosen-to-make-a-new-trade-offer.wav"/>
            <break time="100"/>
            <audio src="/static/en/please-select-the-type-of-seed-you-wish-to-offer.wav"/>
            <break time="200"/>

            % for i in range(0, len(seed_list)):
            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/{{seed_list[i]}}.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/{{i + 1}}.wav"/>
            % end

            <!--<s>To offer something else, press 9.</s>-->

            <audio src="/static/en/something-went-wrong.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/0.wav"/>
        </prompt>

        % for i in range(0, len(seed_list)):
        <choice event="on_provide_selected" message="/static/en/{{seed_list[i]}}.wav" dtmf="{{i + 1}}"/>
        % end

        <!--<choice event="on_provide_selected_other" message="other" dtmf="9"/>-->
        <choice next="/main_menu.vxml#main_menu" dtmf="0"/>
    </menu>

    <!-- At this stage the user tells the system what seeds they want -->
    <menu id="stage_2">
        <prompt>
            <audio src="you-have-chosen-to-offer"/>
            <audio expr="provide_name"/>
            <break time="100"/>
            <audio src="what-seeds-would-you-like-to-request"/>
            <break time="200"/>

            % for i in range(0, len(seed_list)):
            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/{{seed_list[i]}}.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/{{i + 1}}.wav"/>
            % end

            <!--<s>To offer something else, press 9.</s>-->

            <audio src="/static/en/something-went-wrong.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/0.wav"/>
        </prompt>

        % for i in range(0, len(seed_list)):
        <choice event="on_request_selected" message="/static/en/{{seed_list[i]}}.wav" dtmf="{{i + 1}}"/>
        % end

        <!--<choice event="on_request_selected_other" message="other" dtmf="9"/>-->
        <choice next="#stage_1" dtmf="0"/>
    </menu>

    <!-- At this stage the user tells the system if they have transportation available -->
    <!-- Functionality disabled as a result of feedback: The 'customer' will always pick up -->
    <!--<menu id="stage_3">-->
        <!--<prompt>-->
            <!--<audio src="you-have-chosen-to-offer"/>-->
            <!--<audio expr="provide_name"/>-->
            <!--<break time="100"/>-->

            <!--<audio src="and-want-to-receive"/>-->
            <!--<audio expr="request_name"/>-->
            <!--<break time="100"/>-->
            <!--<p>-->
                <!--<s>Can you transport the seeds to the other person or will they have to come to pick them up?</s>-->
            <!--</p>-->
            <!--<break time="500"/>-->
            <!--<p>-->
                <!--<s>If you can arrange transport, press 1.</s>-->
                <!--<s>If you cannot arrange transport, press 2.</s>-->

                <!--<s>To organise something else, press 9.</s>-->
                <!--<s>To go back, press 0.</s>-->
            <!--</p>-->
        <!--</prompt>-->

        <!--<choice event="on_transport_selected" message="true" dtmf="1"/>-->
        <!--<choice event="on_transport_selected" message="false" dtmf="2"/>-->

        <!--<choice event="on_transport_selected_other" message="" dtmf="9"/>-->
        <!--<choice next="#stage_2" dtmf="0"/>-->
    <!--</menu>-->

    <!-- At this stage we verify with the user that all is ok -->
    <menu id="stage_4">
        <prompt>
            <audio src="/static/en/you-have-chosen-to-offer.wav"/>
            <audio expr="provide_name"/>
            <break time="100"/>

            <audio src="/static/en/and-want-to-receive.wav"/>
            <audio expr="request_name"/>
            <break time="100"/>

            <audio src="/static/en/if-this-is-correct.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/1.wav"/>

            <audio src="/static/en/if-this-is-not-correct.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/2.wav"/>
        </prompt>

        <choice next="#stage_5" dtmf="1"/>
        <choice next="#stage_1" dtmf="2"/>
    </menu>


    <!-- At this stage the user leaves his name, and possibly a small extra message -->
    <form id="stage_5">
        <property name="bargein" value="false"/>
        <record name="audio_name_location" beep="true" maxtime="10s" finalsilence="3000ms" dtmfterm="true"
                type="audio/x-wav">
            <prompt timeout="5s">
                <audio src="/static/en/please-leave-a-short-message.wav"/>
            </prompt>
            <noinput>
                <audio src="/static/en/sorry-i-didnt-hear-anything.wav"/>
            </noinput>
        </record>

        <field name="confirm" type="boolean">
            <prompt>
                <audio src="/static/en/your-message-is.wav"/>
                <break time="100"/>

                <audio expr="audio_name_location"/>
                <break time="100"/>

                <audio src="/static/en/if-this-is-correct.wav"/>
                <audio src="/static/en/post-choice.wav"/>
                <audio src="/static/en/1.wav"/>

                <audio src="/static/en/if-this-is-not-correct.wav"/>
                <audio src="/static/en/post-choice.wav"/>
                <audio src="/static/en/2.wav"/>
            </prompt>
            <filled>
                <if cond="confirm">
                    <data src="/trades/" method="post"
                          namelist="caller_id provide_name request_name audio_name_location"/>
                    <else>
                        <goto next="#stage_5"/>
                    </else>
                </if>
                <goto next="#stage_finished"/>
                <clear/>
            </filled>
        </field>
    </form>

    <!-- At this stage the user is asked if they want to exit or go again -->
    <menu id="stage_finished" scope="dialog" dtmf="true">
        <prompt>
            <audio src="/static/en/your-offer-has-been-recorded.wav"/>
            <break time="100"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/making-another-trade-offer.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/1.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/listening-to-existing-trade-offers.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/2.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/managing-your-current-offers.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/3.wav"/>

            <audio src="/static/en/pre-choice.wav"/>
            <audio src="/static/en/done-with-system.wav"/>
            <audio src="/static/en/post-choice.wav"/>
            <audio src="/static/en/0.wav"/>

        </prompt>
        <choice next="#stage_1" dtmf="1"/>
        <choice next="/main_menu.vxml#request_trade" dtmf="2"/>
        <choice next="/main_menu.vxml#check_trade" dtmf="3"/>
        <choice next="/main_menu.vxml#leave" dtmf="0"/>
    </menu>
</vxml>