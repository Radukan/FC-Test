-- Overhauled Art — Second Nature Fantasy Biome
-- Only references new fantastical assets. Old industrial grey art scrapped.
-- All entries use 256x256 single-frame or 8-frame animated sheets at scale 0.5.

local function sprite(name, w, h, frames, line)
  return {
    filename = "__second-nature__/graphics/entity/industry/" .. name .. ".png",
    width = w or 256, height = h or 256,
    frame_count = frames or 1, line_length = line or 1,
    direction_count = 1, scale = 0.5, shift = {0, -0.5}, apply_projection = false
  }
end

local function anim(name, w, h, frames, line)
  return {
    filename = "__second-nature__/graphics/entity/industry/" .. name .. ".png",
    width = w or 256, height = h or 256,
    frame_count = frames or 8, line_length = line or 8,
    direction_count = 1, scale = 0.5, shift = {0, -0.5}, apply_projection = false
  }
end

return {
  -- Major rebuilt categories (new fantasy graphics)
  ["algae-vat-east"] = sprite("algae-vat-east"),
  ["algae-vat-north"] = sprite("algae-vat-east"),
  ["algae-vat-south"] = sprite("algae-vat-east"),
  ["algae-vat-west"] = sprite("algae-vat-east"),

  ["composter-east"] = anim("composter-east"),
  ["composter-north"] = anim("composter-east"),
  ["composter-south"] = anim("composter-east"),
  ["composter-west"] = anim("composter-east"),

  ["electrolyzer-east"] = anim("electrolyzer-east"),
  ["electrolyzer-north"] = anim("electrolyzer-east"),
  ["electrolyzer-south"] = anim("electrolyzer-east"),
  ["electrolyzer-west"] = anim("electrolyzer-east"),

  ["reclamation-plant-east"] = anim("reclamation-plant-east"),
  ["reclamation-plant-north"] = anim("reclamation-plant-east"),
  ["reclamation-plant-south"] = anim("reclamation-plant-east"),
  ["reclamation-plant-west"] = anim("reclamation-plant-east"),

  ["pyrolyzer-east"] = anim("pyrolyzer-east"),
  ["pyrolyzer-north"] = anim("pyrolyzer-east"),
  ["pyrolyzer-south"] = anim("pyrolyzer-east"),
  ["pyrolyzer-west"] = anim("pyrolyzer-east"),

  ["materials-kiln-east"] = anim("materials-kiln-east"),
  ["materials-kiln-north"] = anim("materials-kiln-east"),
  ["materials-kiln-south"] = anim("materials-kiln-east"),
  ["materials-kiln-west"] = anim("materials-kiln-east"),

  ["seed-disperser-east"] = anim("seed-disperser-east"),
  ["seed-disperser-north"] = anim("seed-disperser-east"),
  ["seed-disperser-south"] = anim("seed-disperser-east"),
  ["seed-disperser-west"] = anim("seed-disperser-east"),

  ["basalt-conditioner-east"] = anim("basalt-conditioner-east"),
  ["basalt-conditioner-north"] = anim("basalt-conditioner-east"),
  ["basalt-conditioner-south"] = anim("basalt-conditioner-east"),
  ["basalt-conditioner-west"] = anim("basalt-conditioner-east"),

  ["hydroponics-bay-east"] = anim("hydroponics-bay-east"),
  ["hydroponics-bay-north"] = anim("hydroponics-bay-east"),
  ["hydroponics-bay-south"] = anim("hydroponics-bay-east"),
  ["hydroponics-bay-west"] = anim("hydroponics-bay-east"),

  ["soil-enricher-east"] = anim("soil-enricher-east"),
  ["soil-enricher-north"] = anim("soil-enricher-east"),
  ["soil-enricher-south"] = anim("soil-enricher-east"),
  ["soil-enricher-west"] = anim("soil-enricher-east"),

  -- Restoration Nexus (new central building)
  ["restoration-nexus-east"] = {
    filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-east.png",
    width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },
  ["restoration-nexus-north"] = {
    filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-east.png",
    width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },
  ["restoration-nexus-south"] = {
    filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-east.png",
    width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },
  ["restoration-nexus-west"] = {
    filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-east.png",
    width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },

  -- Working animations for major rebuilt categories
  ["restoration-nexus-idle"] = {
    filename = "__second-nature__/graphics/entity/restoration_nexus/restoration-nexus-plant-east.png",
    width = 256, height = 256, frame_count = 8, direction_count = 1, line_length = 8,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },

  -- Bloomback (fantastical replacement)
  ["bloomback-east"] = {
    filename = "__second-nature__/graphics/entity/bloomback.png",
    width = 256, height = 256, frame_count = 1, direction_count = 1, line_length = 1,
    scale = 1.0, shift = {0, -0.5}, apply_projection = false
  },

  -- Warden animations (kept existing references but palette redesigned via new sprites)
  ["warden-0-idle"] = {
    filename = "__second-nature__/graphics/entity/industry/warden-0-idle.png",
    width = 246, height = 404, frame_count = 4, direction_count = 8, line_length = 4,
    scale = 0.25, shift = {0.367, -0.078}, apply_projection = false
  },
}
