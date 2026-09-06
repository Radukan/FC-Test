local C = require("shared.constants")
local Model = require("shared.model")
local S = require("scripts.state")
local Network = require("scripts.network")
local mod_gui = require("mod-gui")
local G = {}
local function player_data(player)
  local root = S.root()
  root.players[player.index] = root.players[player.index] or {planet = S.planet(player.surface) or "nauvis", guide = 1}
  return root.players[player.index]
end
local function wrap(parent, name, caption, width, style)
  local label = parent.add({type = "label", name = name, caption = caption, style = style or "sn_body"})
  label.style.maximal_width = width
  label.style.single_line = false
  return label
end
local function separator(parent) parent.add({type = "line", direction = "horizontal"}) end
local function metric(parent, key, width)
  local row = parent.add({type = "flow", name = key, direction = "horizontal"})
  row.style.vertical_align = "center"
  local image = row.add({type = "sprite", sprite = "virtual-signal/sn-" .. key})
  image.style.width, image.style.height = 24, 24
  row.add({type = "label", caption = {"sn-axis." .. key}, style = "sn_metric_name"})
  local bar = row.add({type = "progressbar", name = "bar", value = 0, style = "sn_progress"})
  bar.style.width = math.max(80, width - 300)
  bar.style.color = C.colors[key]
  row.add({type = "label", name = "value", caption = "—", style = "sn_metric_value"})
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
  local title = frame.add({type = "flow", name = "title", direction = "horizontal"})
  title.style.vertical_align = "center"
  title.add({type = "label", caption = {"sn-gui.title"}, style = "frame_title", ignored_by_interaction = true})
  local drag = title.add({type = "empty-widget", style = "draggable_space_header"})
  drag.style.horizontally_stretchable, drag.style.height = true, 24
  drag.drag_target = frame
  title.add({type = "sprite-button", name = "sn_close", sprite = "utility/close", style = "frame_action_button", tooltip = {"gui.close"}})
  local tabs = frame.add({type = "tabbed-pane", name = "tabs"})
  local function tab(name, caption)
    local label = tabs.add({type = "tab", caption = caption})
    local pane = tabs.add({type = "scroll-pane", name = name, horizontal_scroll_policy = "never"})
    pane.style.maximal_height, pane.style.width = height - 120, width - 32
    tabs.add_tab(label, pane)
    return pane.add({type = "flow", name = "content", direction = "vertical", style = "sn_panel"})
  end
  local overview = tab("overview", {"sn-gui.field-station"})
  local selector = overview.add({type = "flow", name = "selector", direction = "horizontal"})
  local options = {}
  for _, name in ipairs(C.planets) do options[#options + 1] = {"space-location-name." .. name} end
  selector.add({type = "drop-down", name = "sn_planet", items = options, selected_index = selected_index(prefs.planet)})
  selector.add({type = "button", name = "sn_current_planet", caption = {"sn-gui.current-planet"}})
  wrap(overview, "brief", {"sn-planet." .. prefs.planet}, width - 80, "sn_muted")
  local status = overview.add({type = "flow", name = "status", direction = "horizontal"})
  status.add({type = "label", name = "phase", caption = "", style = "sn_heading"})
  status.add({type = "label", name = "score", caption = ""})
  wrap(overview, "uncharted", {"sn-gui.uncharted"}, width - 80)
  local body = overview.add({type = "flow", name = "body", direction = "vertical"})
  body.style.vertical_spacing = 8
  local metrics = body.add({type = "flow", name = "metrics", direction = "vertical"})
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
  local network = tab("network", {"sn-gui.living-network"})
  wrap(network, "heading", {"sn-gui.network-heading"}, width - 80, "sn_heading")
  wrap(network, "description", {"sn-gui.network-description"}, width - 80)
  separator(network)
  for _, name in ipairs(C.planets) do
    local row = network.add({type = "flow", name = name, direction = "vertical"})
    row.add({type = "button", name = "sn_select_" .. name, caption = {"space-location-name." .. name}})
    wrap(row, "state", "", width - 80)
  end
  separator(network)
  local progress = network.add({type = "progressbar", name = "progress", value = 0})
  progress.style.width = width - 88
  progress.style.color = C.colors.biodiversity
  wrap(network, "timer", "", width - 80, "sn_heading")
  wrap(network, "reason", "", width - 80)
  local guide = tab("guide", {"sn-gui.field-guide"})
  local topics = {}
  for i = 1, 5 do topics[i] = {"sn-guide.topic-" .. i} end
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
  if player.gui.screen.sn_dashboard then G.close(player) else G.open(player) end
end
local function format(n) return string.format("%.1f", n) end
function G.update(player)
  local frame = player.gui.screen.sn_dashboard
  if not (frame and frame.valid) then return end
  local prefs = player_data(player)
  local world = S.by_planet(prefs.planet)
  local overview = frame.tabs.overview.content
  overview.brief.caption = {"sn-planet." .. prefs.planet}
  overview.uncharted.visible, overview.body.visible, overview.status.visible = not world, world ~= nil, world ~= nil
  if world then
    overview.status.phase.caption = {"sn-stage." .. C.stages[world.stage + 1].name}
    overview.status.score.caption = {"sn-gui.stability", format(world.score)}
    for _, key in ipairs(C.axes) do
      local row = overview.body.metrics[key]
      row.bar.value, row.value.caption = world.values[key] / 100, format(world.values[key]) .. "%"
      row.tooltip = {"", {"sn-axis-description." .. key}, "\n", {"sn-gui.cap", format(Model.cap(world, key))}}
    end
    for _, key in ipairs({"toxicity", "pressure"}) do
      local row = overview.body.metrics[key]
      row.bar.value, row.value.caption = world[key] / 100, format(world[key]) .. "%"
    end
    local requirements = {"", {"sn-gui.next-phase"}, " "}
    if world.stage < 5 then
      requirements[#requirements + 1] = {"sn-stage." .. C.stages[world.stage + 2].name}
      requirements[#requirements + 1] = ": "
      for i, missing in ipairs(Model.requirements(world, world.stage + 1)) do
        if i > 1 then requirements[#requirements + 1] = " · " end
        requirements[#requirements + 1] = {"", {"sn-axis." .. missing.axis}, missing.axis == "toxicity" and " ≤ " or " ≥ ", missing.target}
      end
    else requirements = {"sn-gui.mature"} end
    overview.body.next.caption = requirements
    overview.body.activity.caption = {"sn-gui.activity", world.active_count, world.machine_count, world.cycles, format(world.ambient)}
    overview.body.impact.caption = {"sn-gui.impact", world.restored_tiles, world.grown_trees, math.floor(world.removed_pollution)}
    if world.warning then overview.body.warning.caption = {"sn-gui.raid-in", math.max(0, math.ceil((world.warning.at - game.tick) / 60))}
    elseif C.profiles[world.planet].native then
      local surface = game.surfaces[world.surface_index]
      if settings.global["sn-native-resistance"].value == "off" or (surface and surface.peaceful_mode) then
        overview.body.warning.caption = {"sn-gui.resistance-disabled"}
      else
        overview.body.warning.caption = {"sn-gui.native-rule", {"string-mod-setting.sn-native-resistance-" .. settings.global["sn-native-resistance"].value}, settings.global["sn-grace-minutes"].value}
      end
    else overview.body.warning.caption = {"sn-gui.no-natives"} end
    overview.body.advice.caption = {"sn-gui.operation-rule"}
  end
  local pane = frame.tabs.network.content
  for _, planet in ipairs(C.planets) do
    local w = S.by_planet(planet)
    pane[planet].state.caption = w and {"sn-gui.world-state", {"sn-stage." .. C.stages[w.stage + 1].name}, format(w.score),
      Network.has_beacon(w, player.force.index) and {"sn-gui.beacon-online"} or {"sn-gui.beacon-offline"}} or {"sn-gui.uncharted"}
  end
  local network = S.root().networks[player.force.index] or {held = 0}
  pane.progress.value = network.held / C.victory_ticks
  pane.timer.caption = network.won and {"sn-gui.victory"} or {"sn-gui.hold-time", math.floor(network.held / 3600), math.floor(network.held / 60) % 60}
  local _, reason = Network.status(player.force)
  pane.reason.caption = not settings.global["sn-network-victory"].value and {"sn-gui.victory-disabled"} or reason
end
function G.click(event)
  if not (event.element and event.element.valid) then return end
  local player = game.get_player(event.player_index)
  if not player then return end
  local name = event.element.name
  if name == "sn_open" then G.toggle(player)
  elseif name == "sn_close" then G.close(player)
  elseif name == "sn_current_planet" or name:sub(1, 10) == "sn_select_" then
    local planet = name == "sn_current_planet" and S.planet(player.surface) or name:sub(11)
    if C.profiles[planet] then
      player_data(player).planet = planet
      local frame = player.gui.screen.sn_dashboard
      if frame then frame.tabs.overview.content.selector.sn_planet.selected_index = selected_index(planet); frame.tabs.selected_tab_index = 1; G.update(player) end
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
    frame.tabs.guide.content.heading.caption = {"sn-guide.topic-" .. topic}
    frame.tabs.guide.content.text.caption = {"sn-guide.text-" .. topic}
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
