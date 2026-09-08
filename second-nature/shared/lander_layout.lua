-- Keep the 0.5 collision contract: a visual refit must not move an existing camp.
-- The offline exporter reads the same view as the prototypes and runtime overlay.
return {
  collision_box = {{-4.7, -2.8}, {4.7, 2.8}},
  selection_box = {{-5, -3.1}, {5, 3.1}},
  view = {width = 1024, height = 768, ppu = 80, scale = 0.4, origin = 0.48, frames = 8},
  animation_speed = 0.05,
  art_revision = 2
}
