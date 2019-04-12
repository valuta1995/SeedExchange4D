<?xml version="1.0"?>
<vxml version="{{vxml_version}}">
    <!-- variables (shared between files in the system)-->
    % for var in global_vars:
    <var name="{{var}}"/>
    % end
</vxml>