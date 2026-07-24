%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dynamic Island Wallpaper — JSON Emitter
% Converts symbolic scene dict → JSON atom
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:- module(emit_json, [
    emit_scene_json/1
]).

:- use_module(library(http/json)).
:- use_module(rules).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% emit_scene_json(-JSONAtom)
%
% Produces a JSON atom representing the symbolic scene.
% This is the final output consumed by the renderer.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

emit_scene_json(JSONAtom) :-
    % Get symbolic scene dict from rules.pl
    scene(SceneDict),

    % Write dict to a JSON string (atom)
    with_output_to(string(JSONString),
        json_write_dict(current_output, SceneDict, [width(0)])
    ),

    % Convert string → atom for easy consumption by Python
    atom_string(JSONAtom, JSONString).
