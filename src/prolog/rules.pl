%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dynamic Island Wallpaper — Semantic Rule Engine
% Telemetry → Symbolic Scene DSL (v0.0.1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:- module(rules, [
    scene/1
]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Scene Entry Point
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% scene(SceneJSON)
% Produces a symbolic scene dictionary (later encoded as JSON).
scene(Scene) :-
    % --- Astronomy ---
    sun_alt(SunAlt),
    sun_az(SunAz),
    moon_alt(MoonAlt),
    moon_phase(MoonPhase),

    % --- BOM Telemetry ---
    tide_height(TideH),
    wind_speed(WindMS),
    weather_code(WCode),

    % --- Daily Rhythm ---
    current_time(Now),
    sleep_time(Sleep),
    work_start(WorkStart),
    break_times(BreakList),

    % --- Symbolic Bucketing ---
    sun_height_bucket(SunAlt, SunHeight),
    sunposition_bucket(SunAlt, SunAz, SunPos),
    sky_mode_bucket(SunAlt, SkyMode),
    moon_bucket(MoonAlt, MoonPhase, MoonSymbol),
    stars_rule(SkyMode, MoonSymbol, Stars),

    tide_bucket(TideH, TideState),
    wind_bucket(WindMS, WindState),
    wave_bucket(WindState, WCode, WaveState),
    palette_bucket(SkyMode, Palette),

    daily_state_bucket(Now, WorkStart, BreakList, Sleep, DailyState),

    % --- Construct Scene Dict ---
    Scene = _{
        sunposition: SunPos,
        sun_height: SunHeight,
        sky_mode: SkyMode,
        weather: WCode,
        moon: MoonSymbol,
        stars: Stars,

        tide_state: TideState,
        wind_strength: WindState,
        wave_intensity: WaveState,
        island_palette: Palette,

        daily_state: DailyState,
        version: "0.0.1"
    }.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2. Solar Bucketing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

sun_height_bucket(Alt, none)   :- Alt < 0, !.
sun_height_bucket(Alt, low)    :- Alt < 10, !.
sun_height_bucket(Alt, medium) :- Alt < 35, !.
sun_height_bucket(_, high).

% Hemisphere-aware azimuth bucketing
sunposition_bucket(Alt, _, none) :- Alt < 0, !.
sunposition_bucket(Alt, Az, Pos) :-
    altitude_zone(Alt, Zone),
    azimuth_zone(Az, Dir),
    atomic_list_concat([Zone, Dir], '', Pos).

altitude_zone(A, bottom) :- A < 10, !.
altitude_zone(A, mid)    :- A < 35, !.
altitude_zone(_, top).

azimuth_zone(Az, left)  :- Az > 180, !.
azimuth_zone(_, right).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3. Sky Mode
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

sky_mode_bucket(Alt, night) :- Alt < -6, !.
sky_mode_bucket(Alt, dawn)  :- Alt >= -6, Alt =< 6, !.
sky_mode_bucket(Alt, dusk)  :- Alt >= -6, Alt =< 6, !.  % same band, resolved later
sky_mode_bucket(_, day).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4. Moon Bucketing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

moon_bucket(Alt, _, none) :- Alt < 0, !.
moon_bucket(_, Phase, crescent) :- Phase < 0.25, !.
moon_bucket(_, Phase, half)     :- Phase < 0.50, !.
moon_bucket(_, Phase, gibbous)  :- Phase < 0.75, !.
moon_bucket(_, _, full).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 5. Stars Visibility
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

stars_rule(night, none, true) :- !.
stars_rule(_, _, false).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 6. Tide Bucketing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

tide_bucket(H, low)    :- H < 0.5, !.
tide_bucket(H, medium) :- H < 1.2, !.
tide_bucket(_, high).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 7. Wind Bucketing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

wind_bucket(S, none)   :- S < 2, !.
wind_bucket(S, breeze) :- S < 5, !.
wind_bucket(S, windy)  :- S < 10, !.
wind_bucket(_, strong).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 8. Wave Bucketing (Wind + Weather)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

wave_bucket(strong, _, storm) :- !.
wave_bucket(windy, 3, rough) :- !.   % heavy rain
wave_bucket(windy, _, rough) :- !.
wave_bucket(breeze, _, gentle) :- !.
wave_bucket(_, _, calm).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 9. Palette Bucketing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

palette_bucket(day, day).
palette_bucket(dawn, sunset).
palette_bucket(dusk, sunset).
palette_bucket(night, night).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 10. Daily Rhythm
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

daily_state_bucket(Now, WorkStart, Breaks, Sleep, morning_start) :-
    Now @< WorkStart, !.

daily_state_bucket(Now, WorkStart, _, _, work_start) :-
    Now @>= WorkStart,
    Now @<  WorkStart + 1*3600, !.  % first hour

daily_state_bucket(Now, _, Breaks, _, break_time) :-
    member(B, Breaks),
    abs(Now - B) < 1800, !.  % within 30 min

daily_state_bucket(Now, _, _, Sleep, evening) :-
    Now @< Sleep, !.

daily_state_bucket(_, _, _, _, sleep_time).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% End of rules.pl
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
