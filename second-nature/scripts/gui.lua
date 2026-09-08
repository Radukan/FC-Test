local C = require("shared.constants")
local Model = require("shared.model")
local S = require("scripts.state")
local Network = require("scripts.network")
local Pollution = require("scripts.pollution")
local Natives = require("scripts.natives")
local Upgrades = require("scripts.upgrades")
local Achievements = require("scripts.achievements")
local Milestones = require("shared.achievements")
local mod_gui = require("mod-gui")
local G = {}
local function player_data(player)
  local root = S.root()
  root.players[player.index] = root.players[player.index] or {planet = S.planet(player.surface) or "nauvis", guide = 1}
  return root.players[player.index]
end
local function wrap(parent, name, caption, width, style)
  local label = parent.add({type = "label", name = "sn_" .. name, caption = caption, style = style or "sn_body"})
  label.style.maximal_width = width
  label.style.single_line = false
  return label
end
local function separator(parent) parent.add({type = "line", direction = "horizontal"}) end
local function metric(parent, key, width)
  local row = parent.add({type = "flow", name = "sn_metric_" .. key, direction = "horizontal"})
  row.style.vertical_align = "center"
  local image = row.add({type = "sprite", sprite = "virtual-signal/sn-" .. key})
  image.style.width, image.style.height = 24, 24
  row.add({type = "label", caption = {"sn-axis." .. key}, style = "sn_metric_name"})
  local bar = row.add({type = "progressbar", name = "sn_bar", value = 0, style = "sn_progress"})
  bar.style.width = math.max(80, width - 300)
  bar.style.color = C.colors[key]
  row.add({type = "label", name = "sn_value", caption = " - ", style = "sn_metric_value"})
  row.tooltip = {"sn-axis-description." .. key}
end
local function selected_index(name)
  for index, planet in ipairs(C.planets) do if name == planet then return index end end
  return 1
end
function G.button(player)
  local flow = mod_gui.get_button_flow(player)
  if not flow.sn_open then flow.add({type = "sprite-button", name = "sn_open", sprite = "sn-logo", style = mod_gui.button_style, tooltip = {"sn-gui.toggle"}}) end
end
function G.close(player)
  local prefs = S.root().players[player.index]
  if prefs then prefs.pending_fate = nil end
  local frame = player.gui.screen.sn_dashboard
  if frame then frame.destroy() end
  player.set_shortcut_toggled("sn-dashboard", false)
end
function G.open(player)
  if player.gui.screen.sn_dashboard then G.close(player) end
  local prefs = player_data(player)
  local width = math.max(440, math.min(780, math.floor(player.display_resolution.width / player.display_scale) - 50))
  local height = math.max(350, math.min(790, math.floor(player.display_resolution.height / player.display_scale) - 70))
  local frame = player.gui.screen.add({type = "frame", name = "sn_dashboard", direction = "vertical"})
  frame.style.width, frame.style.maximal_height = width, height
  frame.auto_center = true
  local title = frame.add({type = "flow", name = "sn_title", direction = "horizontal"})
  title.style.vertical_align = "center"
  title.add({type = "label", caption = {"sn-gui.title"}, style = "frame_title", ignored_by_interaction = true})
  local drag = title.add({type = "empty-widget", style = "draggable_space_header"})
  drag.style.horizontally_stretchable, drag.style.height = true, 24
  drag.drag_target = frame
  title.add({type = "sprite-button", name = "sn_close", sprite = "utility/close", style = "frame_action_button", tooltip = {"gui.close"}})
  local tabs = frame.add({type = "tabbed-pane", name = "sn_tabs"})
  local function tab(name, caption)
    local label = tabs.add({type = "tab", caption = caption})
    local pane = tabs.add({type = "scroll-pane", name = "sn_" .. name, horizontal_scroll_policy = "never"})
    pane.style.maximal_height, pane.style.width = height - 120, width - 32
    tabs.add_tab(label, pane)
    return pane.add({type = "flow", name = "sn_content", direction = "vertical", style = "sn_panel"})
  end
  local overview = tab("overview", {"sn-gui.field-station"})
  local selector = overview.add({type = "flow", name = "sn_selector", direction = "horizontal"})
  local options = {}
  for _, name in ipairs(C.planets) do options[#options + 1] = {"space-location-name." .. name} end
  selector.add({type = "drop-down", name = "sn_planet", items = options, selected_index = selected_index(prefs.planet)})
  selector.add({type = "button", name = "sn_current_planet", caption = {"sn-gui.current-planet"}})
  wrap(overview, "brief", {"sn-planet." .. prefs.planet}, width - 80, "sn_muted")
  local status = overview.add({type = "flow", name = "sn_status", direction = "horizontal"})
  status.add({type = "label", name = "sn_phase", caption = "", style = "sn_heading"})
  status.add({type = "label", name = "sn_score", caption = ""})
  wrap(overview, "uncharted", {"sn-gui.uncharted"}, width - 80)
  local body = overview.add({type = "flow", name = "sn_body", direction = "vertical"})
  body.style.vertical_spacing = 8
  local metrics = body.add({type = "flow", name = "sn_metrics", direction = "vertical"})
  for _, axis in ipairs(C.axes) do metric(metrics, axis, width - 70) end
  separator(body)
  metric(metrics, "toxicity", width - 70)
  metric(metrics, "pressure", width - 70)
  wrap(body, "next", "", width - 80)
  wrap(body, "support", {"sn-gui.support-hint"}, width - 80, "sn_muted")
  separator(body)
  wrap(body, "activity", "", width - 80)
  wrap(body, "impact", "", width - 80, "sn_muted")
  wrap(body, "warning", "", width - 80)
  wrap(body, "advice", "", width - 80, "sn_muted")
  local air = tab("air", {"sn-gui.air-survey"})
  wrap(air, "air_intro", {"sn-air.intro"}, width - 80)
  wrap(air, "air_world", "", width - 80, "sn_heading")
  wrap(air, "air_total", "", width - 80)
  wrap(air, "air_survey", "", width - 80)
  wrap(air, "air_local", "", width - 80)
  wrap(air, "habitat", "", width - 80)
  air.add({type = "button", name = "sn_toggle_overlay", caption = {"sn-air.overlay-off"}})
  wrap(air, "air_legend", {"sn-air.legend"}, width - 80, "sn_muted")
  separator(air)
  wrap(air, "mission", "", width - 80)
  wrap(air, "fate", "", width - 80, "sn_heading")
  wrap(air, "fate_help", {"sn-native.explanation"}, width - 80)
  local choices = air.add({type = "flow", name = "sn_fate_actions", direction = "horizontal"})
  choices.add({type = "button", name = "sn_choose_symbiosis", caption = {"sn-native.symbiosis"}})
  choices.add({type = "button", name = "sn_choose_eradication", caption = {"sn-native.eradication"}})
  wrap(air, "fate_confirm", "", width - 80)
  local confirm = air.add({type = "flow", name = "sn_confirmation", direction = "horizontal"})
  confirm.add({type = "button", name = "sn_confirm_fate", caption = {"sn-native.confirm-button"}})
  confirm.add({type = "button", name = "sn_cancel_fate", caption = {"sn-native.cancel-button"}})
  local network = tab("network", {"sn-gui.living-network"})
  wrap(network, "heading", {"sn-gui.network-heading"}, width - 80, "sn_heading")
  wrap(network, "description", {"sn-gui.network-description"}, width - 80)
  separator(network)
  for _, name in ipairs(C.planets) do
    local row = network.add({type = "flow", name = "sn_world_" .. name, direction = "vertical"})
    row.add({type = "button", name = "sn_select_" .. name, caption = {"space-location-name." .. name}})
    wrap(row, "state", "", width - 80)
  end
  separator(network)
  local progress = network.add({type = "progressbar", name = "sn_progress", value = 0})
  progress.style.width = width - 88
  progress.style.color = C.colors.biodiversity
  wrap(network, "timer", "", width - 80, "sn_heading")
  wrap(network, "reason", "", width - 80)
  local milestones = tab("milestones", {"sn-gui.milestones"})
  wrap(milestones, "milestone_intro", {"sn-gui.milestone-intro"}, width - 80, "sn_muted")
  wrap(milestones, "milestone_count", "", width - 80, "sn_heading")
  for _, entry in ipairs(Milestones.script) do
    local row = milestones.add({type = "flow", name = "sn_medal_" .. entry.name, direction = "horizontal"})
    row.style.vertical_align = "center"
    row.style.horizontal_spacing = 10
    local badge = row.add({type = "sprite", name = "sn_badge", sprite = "sn-medal-" .. entry.name})
    badge.style.width, badge.style.height = 40, 40
    local text = row.add({type = "flow", name = "sn_text", direction = "vertical"})
    text.style.vertical_spacing = 0
    wrap(text, "title", {"achievement-name.sn-" .. entry.name}, width - 150, "sn_heading")
    wrap(text, "detail", {"achievement-description.sn-" .. entry.name}, width - 150, "sn_muted")
  end
  separator(milestones)
  wrap(milestones, "milestone_note", {"sn-gui.milestone-note"}, width - 80, "sn_muted")
  local guide = tab("guide", {"sn-gui.field-guide"})
  local topics = {}
  for i = 1, 6 do topics[i] = {"sn-guide.topic-" .. i} end
  guide.add({type = "drop-down", name = "sn_guide", items = topics, selected_index = prefs.guide})
  wrap(guide, "heading", {"sn-guide.topic-" .. prefs.guide}, width - 80, "sn_heading")
  wrap(guide, "text", {"sn-guide.text-" .. prefs.guide}, width - 80)
  wrap(frame, "footer", {"sn-gui.footer"}, width - 44, "sn_muted")
  tabs.selected_tab_index = 1
  player.opened = frame
  player.set_shortcut_toggled("sn-dashboard", true)
  G.update(player)
end
function G.toggle(player)
  if not player then return end
  local ok, err = pcall(function()
    if player.gui.screen.sn_dashboard then G.close(player) else G.open(player) end
  end)
  if not ok then
    -- A presentation bug must never take down a multiplayer factory.
    local frame = player.gui.screen.sn_dashboard
    if frame and frame.valid then frame.destroy() end
    player.set_shortcut_toggled("sn-dashboard", false)
    log("Second Nature dashboard: " .. tostring(err))
    player.print({"sn-gui.ui-error"})
  end
end
function G.toggle_overlay(player)
  if not player then return end
  local prefs = player_data(player)
  prefs.air_overlay = not prefs.air_overlay
  player.set_shortcut_toggled("sn-pollution-overlay", prefs.air_overlay)
  Pollution.overlay(player, prefs.air_overlay)
  G.update(player)
end
local function format(n) return string.format("%.1f", n) end
function G.update(player)
  local frame = player.gui.screen.sn_dashboard
  if not (frame and frame.valid) then return end
  local prefs = player_data(player)
  local world = S.by_planet(prefs.planet)
  local overview = frame.sn_tabs.sn_overview.sn_content
  overview.sn_brief.caption = {"sn-planet." .. prefs.planet}
  overview.sn_uncharted.visible, overview.sn_body.visible, overview.sn_status.visible = not world, world ~= nil, world ~= nil
  if world then
    overview.sn_status.sn_phase.caption = {"sn-stage." .. C.stages[world.stage + 1].name}
    overview.sn_status.sn_score.caption = {"sn-gui.stability", format(world.score)}
    for _, key in ipairs(C.axes) do
      local row = overview.sn_body.sn_metrics["sn_metric_" .. key]
      row.sn_bar.value, row.sn_value.caption = world.values[key] / 100, format(world.values[key]) .. "%"
      row.tooltip = {"", {"sn-axis-description." .. key}, "\n", {"sn-gui.cap", format(Model.cap(world, key))}}
    end
    for _, key in ipairs({"toxicity", "pressure"}) do
      local row = overview.sn_body.sn_metrics["sn_metric_" .. key]
      row.sn_bar.value, row.sn_value.caption = world[key] / 100, format(world[key]) .. "%"
    end
    local requirements = {"", {"sn-gui.next-phase"}, " "}
    if world.stage < 5 then
      requirements[#requirements + 1] = {"sn-stage." .. C.stages[world.stage + 2].name}
      requirements[#requirements + 1] = ": "
      for i, missing in ipairs(Model.requirements(world, world.stage + 1)) do
        if i > 1 then requirements[#requirements + 1] = " · " end
        requirements[#requirements + 1] = {"", {"sn-axis." .. missing.axis}, (missing.less or missing.axis == "toxicity") and " ≤ " or " ≥ ", missing.target}
      end
    else requirements = {"sn-gui.mature"} end
    overview.sn_body.sn_next.caption = requirements
    overview.sn_body.sn_activity.caption = {"sn-gui.activity", world.active_count, world.machine_count, world.cycles, format(world.ambient)}
    overview.sn_body.sn_impact.caption = {"sn-gui.impact", world.restored_tiles, world.grown_trees, math.floor(world.removed_pollution)}
    if world.native_outcome then overview.sn_body.sn_warning.caption = {"sn-native.resolved-" .. world.native_outcome.mode, world.native_outcome.processed}
    elseif world.warning then overview.sn_body.sn_warning.caption = {"sn-gui.raid-in", math.max(0, math.ceil((world.warning.at - game.tick) / 60))}
    elseif C.profiles[world.planet].native then
      local surface = game.surfaces[world.surface_index]
      if settings.global["sn-native-resistance"].value == "off" or (surface and surface.peaceful_mode) then
        overview.sn_body.sn_warning.caption = {"sn-gui.resistance-disabled"}
      else
        overview.sn_body.sn_warning.caption = {"sn-gui.native-rule", {"string-mod-setting.sn-native-resistance-" .. settings.global["sn-native-resistance"].value}, settings.global["sn-grace-minutes"].value}
      end
    else overview.sn_body.sn_warning.caption = {"sn-gui.no-natives"} end
    overview.sn_body.sn_advice.caption = {"sn-gui.operation-rule"}
  end
  local air_pane = frame.sn_tabs.sn_air.sn_content
  local air = world and world.air
  air_pane.sn_air_world.caption = {"space-location-name." .. prefs.planet}
  air_pane.sn_air_total.caption = air and {"sn-air.total", format(air.total), format(air.trend), format(air.mean), C.air.total_goal} or {"sn-gui.uncharted"}
  air_pane.sn_air_survey.caption = air and {"sn-air.survey", #(world.chunks or {}), air.dirty, format(math.max(air.peak, air.scan_peak or 0)),
    air.survey_complete and {"sn-air.complete"} or {"sn-air.pending"}, math.max(0, math.floor((game.tick - air.sampled_at) / 60))} or ""
  local here = S.planet(player.surface)
  local local_pollution = Pollution.local_amount(player.surface, player.position)
  air_pane.sn_air_local.caption = {"sn-air.local", here and {"space-location-name." .. here} or player.surface.name,
    format(local_pollution), here == "nauvis" and math.floor(Pollution.calm(player.surface, player.position) * 100) or 0}
  air_pane.sn_habitat.caption = {"sn-expedition.habitat-status", world and world.landscape and format(world.landscape.mean * 100) or " - ",
    C.pace.landscape_goal * 100, math.floor((Upgrades.bonus(player.force) - 1) * 100 + .5)}
  air_pane.sn_toggle_overlay.caption = {prefs.air_overlay and "sn-air.overlay-on" or "sn-air.overlay-off"}
  local camp = S.root().campaign and S.root().campaign.camps[player.force.index]
  air_pane.sn_mission.caption = camp and {camp.rocket_launched and "sn-campaign.mission-orbit" or "sn-campaign.mission-stranded"} or {"sn-campaign.mission-existing"}
  local nauvis = S.by_planet("nauvis")
  local outcome = nauvis and nauvis.native_outcome
  air_pane.sn_fate.caption = outcome and {"sn-native.resolved-" .. outcome.mode, outcome.processed} or {"sn-native.waiting"}
  local can_choose = Natives.available(nauvis) and (not game.is_multiplayer() or player.admin)
  air_pane.sn_fate_actions.sn_choose_symbiosis.enabled = not not can_choose
  air_pane.sn_fate_actions.sn_choose_eradication.enabled = not not can_choose
  if not can_choose then prefs.pending_fate = nil end
  air_pane.sn_fate_confirm.visible = prefs.pending_fate ~= nil
  air_pane.sn_confirmation.visible = prefs.pending_fate ~= nil
  if prefs.pending_fate then air_pane.sn_fate_confirm.caption = {"sn-native.confirm-" .. prefs.pending_fate} end
  local pane = frame.sn_tabs.sn_network.sn_content
  for _, planet in ipairs(C.planets) do
    local w = S.by_planet(planet)
    pane["sn_world_" .. planet].sn_state.caption = w and {"sn-gui.world-state", {"sn-stage." .. C.stages[w.stage + 1].name}, format(w.score),
      Network.has_beacon(w, player.force.index) and {"sn-gui.beacon-online"} or {"sn-gui.beacon-offline"}} or {"sn-gui.uncharted"}
  end
  local medals = frame.sn_tabs.sn_milestones.sn_content
  local earned, total = Achievements.count(player.force.index)
  medals.sn_milestone_count.caption = {"sn-gui.milestone-count", earned, total}
  for _, entry in ipairs(Milestones.script) do
    local row = medals["sn_medal_" .. entry.name]
    local held = Achievements.earned(player.force.index, entry.name)
    -- Locked medallions stay visible so the goal itself is readable, but they
    -- are drawn in grey and only show their real elapsed time once earned.
    row.sn_badge.style.draw_grayscale_picture = not held
    row.sn_text.sn_title.style.font_color = held and {0.68, 0.9, 0.64} or {0.62, 0.65, 0.62}
    if held then
      local at = S.root().achievements.forces[player.force.index][entry.name] or game.tick
      row.sn_text.sn_detail.caption = {"sn-gui.milestone-when", math.floor((game.tick - at) / 3600)}
    else
      row.sn_text.sn_detail.caption = {"achievement-description.sn-" .. entry.name}
    end
  end
  local network = S.root().networks[player.force.index] or {held = 0}
  pane.sn_progress.value = network.held / C.victory_ticks
  pane.sn_timer.caption = network.won and {"sn-gui.victory"} or {"sn-gui.hold-time", math.floor(network.held / 3600), math.floor(network.held / 60) % 60}
  local _, reason = Network.status(player.force)
  pane.sn_reason.caption = not settings.global["sn-network-victory"].value and {"sn-gui.victory-disabled"} or reason
end
function G.click(event)
  if not (event.element and event.element.valid) then return end
  local player = game.get_player(event.player_index)
  if not player then return end
  local name = event.element.name
  if name == "sn_toggle_overlay" then G.toggle_overlay(player)
  elseif name == "sn_choose_symbiosis" or name == "sn_choose_eradication" then
    local prefs = player_data(player)
    if Natives.available(S.by_planet("nauvis")) then prefs.pending_fate = name:sub(11) end
    G.update(player)
  elseif name == "sn_cancel_fate" then player_data(player).pending_fate = nil; G.update(player)
  elseif name == "sn_confirm_fate" then
    local prefs = player_data(player)
    if prefs.pending_fate then Natives.choose(S.by_planet("nauvis"), prefs.pending_fate, player) end
    prefs.pending_fate = nil; G.update(player)
  elseif name == "sn_open" then G.toggle(player)
  elseif name == "sn_close" then G.close(player)
  elseif name == "sn_current_planet" or name:sub(1, 10) == "sn_select_" then
    local planet = name == "sn_current_planet" and S.planet(player.surface) or name:sub(11)
    if C.profiles[planet] then
      player_data(player).planet = planet
      local frame = player.gui.screen.sn_dashboard
      if frame then frame.sn_tabs.sn_overview.sn_content.sn_selector.sn_planet.selected_index = selected_index(planet); frame.sn_tabs.selected_tab_index = 1; G.update(player) end
    end
  end
end
function G.selection(event)
  if not (event.element and event.element.valid) then return end
  local player = game.get_player(event.player_index)
  local frame = player and player.gui.screen.sn_dashboard
  if not frame then return end
  if event.element.name == "sn_planet" then
    player_data(player).planet = C.planets[event.element.selected_index]
    G.update(player)
  elseif event.element.name == "sn_guide" then
    local topic = event.element.selected_index
    player_data(player).guide = topic
    frame.sn_tabs.sn_guide.sn_content.sn_heading.caption = {"sn-guide.topic-" .. topic}
    frame.sn_tabs.sn_guide.sn_content.sn_text.caption = {"sn-guide.text-" .. topic}
  end
end
function G.welcome(player)
  G.button(player)
  local prefs = player_data(player)
  if not prefs.welcomed and settings.get_player_settings(player)["sn-show-welcome"].value then
    player.print({"sn-message.welcome"}, {color = C.colors.biodiversity})
  end
  prefs.welcomed = true
end
return G
