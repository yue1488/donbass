"""Single source of truth for blocks and items of the Donbass mod.

Everything else (Java registries, blockstates, models, loot tables, recipes,
tags, lang files) is generated from the tables in this file by gen_resources.py.
Names are (en, ru, pl).
"""

MOD_ID = "donbass"

# ---------------------------------------------------------------- blocks ----
# kind: cube | pillar | slab | stairs | pane | glass | falling | magma
# props: (mapColor, hardness, resistance, sound, needs_tool, light)
# tex:   cube -> "name";  pillar -> ("side", "end");  pane -> "name"
# loot:  "self" | ("ore", item, min, max, fortune)   (ore blocks give self with silk touch)
# tool:  pickaxe | shovel | axe ;  tier: None | stone | iron
BLOCKS = []


def block(id, names, kind="cube", tex=None, props=("STONE", 2.0, 6.0, "STONE", True, 0),
          loot="self", tool="pickaxe", tier=None, base=None, falling_color=None):
    BLOCKS.append(dict(id=id, names=names, kind=kind, tex=tex or id, props=props, loot=loot,
                       tool=tool, tier=tier, base=base, falling_color=falling_color))


# --- mine concrete & slag ---------------------------------------------------
block("mine_concrete", ("Mine Concrete", "Шахтный бетон", "Beton górniczy"),
      props=("COLOR_GRAY", 3.0, 9.0, "STONE", True, 0))
block("reinforced_mine_concrete", ("Reinforced Mine Concrete", "Армированный шахтный бетон", "Zbrojony beton górniczy"),
      props=("COLOR_GRAY", 5.0, 30.0, "STONE", True, 0), tier="stone")
block("cracked_mine_concrete", ("Cracked Mine Concrete", "Потрескавшийся шахтный бетон", "Popękany beton górniczy"),
      props=("COLOR_GRAY", 2.0, 5.0, "STONE", True, 0))
block("soot_stained_concrete", ("Soot-Stained Concrete", "Закопчённый бетон", "Okopcony beton"),
      props=("COLOR_BLACK", 3.0, 9.0, "STONE", True, 0))
block("mine_concrete_slab", ("Mine Concrete Slab", "Плита из шахтного бетона", "Płyta z betonu górniczego"),
      kind="slab", base="mine_concrete", props=("COLOR_GRAY", 3.0, 9.0, "STONE", True, 0))
block("mine_concrete_stairs", ("Mine Concrete Stairs", "Ступени из шахтного бетона", "Schody z betonu górniczego"),
      kind="stairs", base="mine_concrete", props=("COLOR_GRAY", 3.0, 9.0, "STONE", True, 0))

block("slag_block", ("Slag Block", "Шлакоблок", "Pustak żużlowy"),
      props=("COLOR_GRAY", 2.0, 6.0, "STONE", True, 0))
block("slag_bricks", ("Slag Bricks", "Шлаковый кирпич", "Cegły żużlowe"),
      props=("COLOR_GRAY", 2.0, 6.0, "STONE", True, 0))
block("polished_slag", ("Polished Slag", "Полированный шлак", "Polerowany żużel"),
      props=("COLOR_GRAY", 2.0, 6.0, "STONE", True, 0))
block("slag_bricks_slab", ("Slag Brick Slab", "Плита из шлакового кирпича", "Płyta z cegły żużlowej"),
      kind="slab", base="slag_bricks", props=("COLOR_GRAY", 2.0, 6.0, "STONE", True, 0))
block("slag_bricks_stairs", ("Slag Brick Stairs", "Ступени из шлакового кирпича", "Schody z cegły żużlowej"),
      kind="stairs", base="slag_bricks", props=("COLOR_GRAY", 2.0, 6.0, "STONE", True, 0))

# --- industrial & housing materials ----------------------------------------
block("sooty_bricks", ("Sooty Bricks", "Закопчённый кирпич", "Okopcone cegły"),
      props=("TERRACOTTA_BROWN", 2.0, 6.0, "STONE", True, 0))
block("whitewashed_wall", ("Whitewashed Wall", "Побелённая стена", "Bielona ściana"),
      props=("SNOW", 1.5, 4.0, "STONE", True, 0))
block("clay_plaster", ("Clay Plaster", "Глиняная обмазка", "Tynk gliniany"),
      props=("TERRACOTTA_YELLOW", 1.0, 3.0, "GRAVEL", False, 0), tool="shovel")
block("prefab_panel", ("Prefab Panel", "Панельная плита", "Płyta prefabrykowana"),
      props=("COLOR_LIGHT_GRAY", 3.0, 9.0, "STONE", True, 0))
block("slate_roof", ("Slate Roof Sheet", "Шифер", "Eternit falisty"),
      props=("COLOR_LIGHT_GRAY", 1.5, 4.0, "STONE", True, 0))
block("rusty_iron_block", ("Rusty Iron Block", "Ржавый железный блок", "Zardzewiały blok żelaza"),
      props=("COLOR_ORANGE", 4.0, 12.0, "METAL", True, 0))
block("rusty_plate", ("Rusty Plating", "Ржавая обшивка", "Zardzewiała blacha"),
      props=("COLOR_ORANGE", 3.0, 9.0, "METAL", True, 0))
block("factory_glass", ("Factory Glass", "Заводское стекло", "Szkło fabryczne"),
      kind="glass", props=("NONE", 0.4, 0.4, "GLASS", False, 0))
block("rusty_fence", ("Rusty Fence", "Ржавое ограждение", "Zardzewiałe ogrodzenie"),
      kind="pane", tex="rusty_fence", props=("COLOR_ORANGE", 2.0, 6.0, "METAL", True, 0))
block("chimney_bricks", ("Chimney Bricks", "Кирпич дымовой трубы", "Cegła kominowa"),
      props=("TERRACOTTA_RED", 2.0, 6.0, "STONE", True, 0))
block("hazard_stripes", ("Hazard Stripes", "Сигнальная разметка", "Oznakowanie ostrzegawcze"),
      props=("COLOR_YELLOW", 2.0, 6.0, "STONE", True, 0))
block("steel_girder", ("Steel Girder", "Стальная балка", "Dźwigar stalowy"),
      kind="pillar", tex=("steel_girder_side", "steel_girder_end"),
      props=("METAL", 4.0, 12.0, "METAL", True, 0))

# --- terricones & spoil -----------------------------------------------------
block("spoil_rock", ("Spoil Rock", "Порода терриконов", "Skała płonna"),
      props=("COLOR_GRAY", 1.5, 4.0, "STONE", True, 0))
block("burnt_spoil", ("Burnt Spoil", "Горелая порода", "Przepalona skała płonna"),
      props=("TERRACOTTA_RED", 1.5, 4.0, "STONE", True, 0))
block("spoil_gravel", ("Spoil Heap Gravel", "Отвальный щебень", "Żwir hałdowy"),
      kind="falling", props=("COLOR_GRAY", 0.7, 0.7, "GRAVEL", False, 0), tool="shovel", falling_color=0x3F3F3F)
block("coal_shale", ("Coal Shale", "Углистый сланец", "Łupek węglowy"),
      props=("COLOR_BLACK", 2.0, 5.0, "STONE", True, 0),
      loot=("ore", "coal_dust", 1, 2, True))
block("smoldering_spoil", ("Smoldering Spoil", "Тлеющая порода", "Tlący się odpad"),
      kind="magma", props=("COLOR_RED", 0.8, 0.8, "STONE", True, 6))

# --- ores -------------------------------------------------------------------
block("coal_seam", ("Coal Seam", "Угольный пласт", "Pokład węgla"),
      props=("STONE", 3.0, 3.0, "STONE", True, 0),
      loot=("ore", "minecraft:coal", 1, 3, True))
block("anthracite_ore", ("Anthracite Ore", "Антрацитовая руда", "Ruda antracytu"),
      props=("STONE", 3.5, 3.5, "STONE", True, 0), tier="stone",
      loot=("ore", "anthracite", 1, 2, True))
block("deepslate_anthracite_ore", ("Deepslate Anthracite Ore", "Глубинная антрацитовая руда", "Ruda antracytu w łupku głębinowym"),
      props=("DEEPSLATE", 4.5, 3.5, "DEEPSLATE", True, 0), tier="stone",
      loot=("ore", "anthracite", 1, 3, True))
block("anthracite_block", ("Block of Anthracite", "Антрацитовый блок", "Blok antracytu"),
      props=("COLOR_BLACK", 5.0, 6.0, "STONE", True, 0))
block("coke_block", ("Block of Coke", "Коксовый блок", "Blok koksu"),
      props=("COLOR_GRAY", 5.0, 6.0, "STONE", True, 0))
block("coal_bunker", ("Coal Bunker", "Угольный бункер", "Zasobnik węgla"),
      props=("METAL", 3.0, 6.0, "METAL", True, 0))

# --- mine equipment ---------------------------------------------------------
block("mine_timber_beam", ("Mine Timber Beam", "Шахтная стойка", "Stempel drewniany"),
      kind="pillar", tex=("mine_timber_beam_side", "mine_timber_beam_end"),
      props=("WOOD", 2.0, 3.0, "WOOD", False, 0), tool="axe")
block("mine_timber_planks", ("Mine Timber Planks", "Шахтный крепёжный лес", "Okładzina stemplowa"),
      props=("WOOD", 2.0, 3.0, "WOOD", False, 0), tool="axe")
block("mine_lamp", ("Mine Lamp", "Шахтный светильник", "Lampa górnicza"),
      props=("METAL", 1.0, 3.0, "METAL", False, 15))
block("ventilation_grate", ("Ventilation Grate", "Вентиляционная решётка", "Kratka wentylacyjna"),
      props=("METAL", 3.0, 6.0, "METAL", True, 0))

# --- railway ----------------------------------------------------------------
block("railway_ballast", ("Railway Ballast", "Железнодорожный балласт", "Podsypka kolejowa"),
      props=("COLOR_GRAY", 0.8, 0.8, "GRAVEL", False, 0), tool="shovel")
block("rail_sleepers", ("Rail Sleepers", "Шпалы", "Podkłady kolejowe"),
      kind="pillar", tex=("rail_sleepers_side", "rail_sleepers_end"),
      props=("COLOR_BROWN", 2.0, 3.0, "WOOD", False, 0), tool="axe")
block("freight_wagon_plating", ("Freight Wagon Plating", "Обшивка грузового вагона", "Poszycie wagonu towarowego"),
      props=("TERRACOTTA_RED", 3.0, 9.0, "METAL", True, 0))

# ----------------------------------------------------------------- items ----
# kind: plain | food | fuel | ticket
ITEMS = []


def item(id, names, kind="plain", burn=0, nutrition=0, sat=0.0):
    ITEMS.append(dict(id=id, names=names, kind=kind, burn=burn, nutrition=nutrition, sat=sat))


item("anthracite", ("Anthracite", "Антрацит", "Antracyt"), kind="fuel", burn=3200)
item("coke", ("Coke", "Кокс", "Koks"), kind="fuel", burn=2400)
item("coal_dust", ("Coal Dust", "Угольная пыль", "Pył węglowy"), kind="fuel", burn=400)
item("slag", ("Slag", "Шлак", "Żużel"))
item("iron_scrap", ("Iron Scrap", "Железный лом", "Złom żelaza"))
item("rusty_gear", ("Rusty Gear", "Ржавая шестерня", "Zardzewiałe koło zębate"))
item("miners_token", ("Miner's Token", "Жетон шахтёра", "Żeton górnika"))
item("miners_ration", ("Miner's Ration", "Шахтёрский паёк", "Racja górnika"), kind="food", nutrition=8, sat=0.8)
item("donbass_ticket", ("Donbass Travel Voucher", "Путёвка в Донбасс", "Skierowanie do Donbasu"), kind="ticket")
item("miners_pickaxe", ("Miner's Pickaxe", "Шахтёрская кирка", "Kilof górniczy"), kind="pickaxe")

# creative tab / misc keys
LANG_EXTRA = {
    "itemGroup.donbass": ("Donbass", "Донбасс", "Donbas"),
    "biome.donbass.steppe": ("Donbass Steppe", "Донбасская степь", "Step donbaski"),
    "biome.donbass.balka": ("Balka Gully", "Балка", "Bałka (jar stepowy)"),
    "message.donbass.travel_to": ("The steppe wind carries you to the Donbass...", "Степной ветер несёт вас на Донбасс...", "Stepowy wiatr niesie cię do Donbasu..."),
    "message.donbass.travel_back": ("You return from the Donbass.", "Вы возвращаетесь с Донбасса.", "Wracasz z Donbasu."),
    "message.donbass.wrong_place": ("The voucher only works in the Overworld and in the Donbass.", "Путёвка действует только в Верхнем мире и на Донбассе.", "Skierowanie działa tylko w Nadświecie i w Donbasie."),
}

# recipes (raw JSON dicts keyed by file name); "donbass:" prefix added where needed
D = "donbass:"
RECIPES = {
    "mine_concrete": {"type": "minecraft:crafting_shaped", "pattern": ["CS", "SC"],
                      "key": {"C": {"item": "minecraft:cobblestone"}, "S": {"item": D + "slag"}},
                      "result": {"item": D + "mine_concrete", "count": 4}},
    "reinforced_mine_concrete": {"type": "minecraft:crafting_shapeless",
                                 "ingredients": [{"item": D + "mine_concrete"}] * 4 + [{"item": "minecraft:iron_ingot"}],
                                 "result": {"item": D + "reinforced_mine_concrete", "count": 4}},
    "cracked_mine_concrete": {"type": "minecraft:smelting", "ingredient": {"item": D + "mine_concrete"},
                              "result": D + "cracked_mine_concrete", "experience": 0.1, "cookingtime": 200},
    "soot_stained_concrete": {"type": "minecraft:crafting_shapeless",
                              "ingredients": [{"item": D + "mine_concrete"}, {"item": D + "coal_dust"}],
                              "result": {"item": D + "soot_stained_concrete", "count": 1}},
    "slag_from_spoil": {"type": "minecraft:smelting", "ingredient": {"item": D + "spoil_rock"},
                        "result": D + "slag", "experience": 0.1, "cookingtime": 200},
    "slag_from_burnt_spoil": {"type": "minecraft:smelting", "ingredient": {"item": D + "burnt_spoil"},
                              "result": D + "slag", "experience": 0.1, "cookingtime": 200},
    "slag_block": {"type": "minecraft:crafting_shaped", "pattern": ["SS", "SS"],
                   "key": {"S": {"item": D + "slag"}}, "result": {"item": D + "slag_block", "count": 4}},
    "slag_bricks": {"type": "minecraft:crafting_shaped", "pattern": ["BB", "BB"],
                    "key": {"B": {"item": D + "slag_block"}}, "result": {"item": D + "slag_bricks", "count": 4}},
    "polished_slag": {"type": "minecraft:crafting_shaped", "pattern": ["BB", "BB"],
                      "key": {"B": {"item": D + "slag_bricks"}}, "result": {"item": D + "polished_slag", "count": 4}},
    "mine_concrete_slab": {"type": "minecraft:crafting_shaped", "pattern": ["CCC"],
                           "key": {"C": {"item": D + "mine_concrete"}}, "result": {"item": D + "mine_concrete_slab", "count": 6}},
    "mine_concrete_stairs": {"type": "minecraft:crafting_shaped", "pattern": ["C  ", "CC ", "CCC"],
                             "key": {"C": {"item": D + "mine_concrete"}}, "result": {"item": D + "mine_concrete_stairs", "count": 4}},
    "slag_bricks_slab": {"type": "minecraft:crafting_shaped", "pattern": ["CCC"],
                         "key": {"C": {"item": D + "slag_bricks"}}, "result": {"item": D + "slag_bricks_slab", "count": 6}},
    "slag_bricks_stairs": {"type": "minecraft:crafting_shaped", "pattern": ["C  ", "CC ", "CCC"],
                           "key": {"C": {"item": D + "slag_bricks"}}, "result": {"item": D + "slag_bricks_stairs", "count": 4}},
    "sooty_bricks": {"type": "minecraft:crafting_shapeless",
                     "ingredients": [{"item": "minecraft:bricks"}, {"item": D + "coal_dust"}],
                     "result": {"item": D + "sooty_bricks", "count": 1}},
    "whitewashed_wall": {"type": "minecraft:crafting_shapeless",
                         "ingredients": [{"item": D + "clay_plaster"}, {"item": "minecraft:bone_meal"}],
                         "result": {"item": D + "whitewashed_wall", "count": 1}},
    "clay_plaster": {"type": "minecraft:crafting_shaped", "pattern": ["CC", "CC"],
                     "key": {"C": {"item": "minecraft:clay_ball"}}, "result": {"item": D + "clay_plaster", "count": 4}},
    "prefab_panel": {"type": "minecraft:crafting_shaped", "pattern": ["CIC", "CCC"],
                     "key": {"C": {"item": D + "mine_concrete"}, "I": {"item": "minecraft:iron_nugget"}},
                     "result": {"item": D + "prefab_panel", "count": 4}},
    "slate_roof": {"type": "minecraft:crafting_shaped", "pattern": ["SSS"],
                   "key": {"S": {"item": D + "polished_slag"}}, "result": {"item": D + "slate_roof", "count": 6}},
    "rusty_iron_block": {"type": "minecraft:crafting_shaped", "pattern": ["SSS", "SSS", "SSS"],
                         "key": {"S": {"item": D + "iron_scrap"}}, "result": {"item": D + "rusty_iron_block", "count": 1}},
    "rusty_plate": {"type": "minecraft:crafting_shapeless",
                    "ingredients": [{"item": D + "rusty_iron_block"}],
                    "result": {"item": D + "rusty_plate", "count": 4}},
    "factory_glass": {"type": "minecraft:crafting_shaped", "pattern": ["GI", "IG"],
                      "key": {"G": {"item": "minecraft:glass"}, "I": {"item": "minecraft:iron_nugget"}},
                      "result": {"item": D + "factory_glass", "count": 4}},
    "rusty_fence": {"type": "minecraft:crafting_shaped", "pattern": ["SSS", "SSS"],
                    "key": {"S": {"item": D + "iron_scrap"}}, "result": {"item": D + "rusty_fence", "count": 8}},
    "chimney_bricks": {"type": "minecraft:crafting_shapeless",
                       "ingredients": [{"item": D + "sooty_bricks"}, {"item": "minecraft:white_concrete_powder"}],
                       "result": {"item": D + "chimney_bricks", "count": 1}},
    "hazard_stripes": {"type": "minecraft:crafting_shapeless",
                       "ingredients": [{"item": D + "mine_concrete"}, {"item": "minecraft:yellow_dye"}, {"item": "minecraft:black_dye"}],
                       "result": {"item": D + "hazard_stripes", "count": 2}},
    "steel_girder": {"type": "minecraft:crafting_shaped", "pattern": ["III", " I ", "III"],
                     "key": {"I": {"item": "minecraft:iron_ingot"}}, "result": {"item": D + "steel_girder", "count": 4}},
    "coal_dust": {"type": "minecraft:crafting_shapeless",
                  "ingredients": [{"item": "minecraft:coal"}], "result": {"item": D + "coal_dust", "count": 2}},
    "coke": {"type": "minecraft:smelting", "ingredient": {"item": "minecraft:coal"},
             "result": D + "coke", "experience": 0.35, "cookingtime": 400},
    "coke_blasting": {"type": "minecraft:blasting", "ingredient": {"item": "minecraft:coal"},
                      "result": D + "coke", "experience": 0.35, "cookingtime": 200},
    "coke_block": {"type": "minecraft:crafting_shaped", "pattern": ["CCC", "CCC", "CCC"],
                   "key": {"C": {"item": D + "coke"}}, "result": {"item": D + "coke_block", "count": 1}},
    "coke_from_block": {"type": "minecraft:crafting_shapeless", "ingredients": [{"item": D + "coke_block"}],
                        "result": {"item": D + "coke", "count": 9}},
    "anthracite_block": {"type": "minecraft:crafting_shaped", "pattern": ["AAA", "AAA", "AAA"],
                         "key": {"A": {"item": D + "anthracite"}}, "result": {"item": D + "anthracite_block", "count": 1}},
    "anthracite_from_block": {"type": "minecraft:crafting_shapeless", "ingredients": [{"item": D + "anthracite_block"}],
                              "result": {"item": D + "anthracite", "count": 9}},
    "anthracite_ore_smelting": {"type": "minecraft:smelting", "ingredient": {"item": D + "anthracite_ore"},
                                "result": D + "anthracite", "experience": 0.2, "cookingtime": 200},
    "anthracite_ore_blasting": {"type": "minecraft:blasting", "ingredient": {"item": D + "anthracite_ore"},
                                "result": D + "anthracite", "experience": 0.2, "cookingtime": 100},
    "deepslate_anthracite_ore_smelting": {"type": "minecraft:smelting", "ingredient": {"item": D + "deepslate_anthracite_ore"},
                                          "result": D + "anthracite", "experience": 0.2, "cookingtime": 200},
    "deepslate_anthracite_ore_blasting": {"type": "minecraft:blasting", "ingredient": {"item": D + "deepslate_anthracite_ore"},
                                          "result": D + "anthracite", "experience": 0.2, "cookingtime": 100},
    "coal_bunker": {"type": "minecraft:crafting_shaped", "pattern": ["I I", "ICI", "III"],
                    "key": {"I": {"item": "minecraft:iron_ingot"}, "C": {"item": "minecraft:coal_block"}},
                    "result": {"item": D + "coal_bunker", "count": 1}},
    "mine_timber_beam": {"type": "minecraft:crafting_shaped", "pattern": ["L", "L"],
                         "key": {"L": {"item": "minecraft:spruce_log"}}, "result": {"item": D + "mine_timber_beam", "count": 3}},
    "mine_timber_planks": {"type": "minecraft:crafting_shapeless",
                           "ingredients": [{"item": D + "mine_timber_beam"}],
                           "result": {"item": D + "mine_timber_planks", "count": 2}},
    "mine_lamp": {"type": "minecraft:crafting_shaped", "pattern": [" I ", "GTG", " I "],
                  "key": {"I": {"item": "minecraft:iron_ingot"}, "G": {"item": "minecraft:glass_pane"}, "T": {"item": "minecraft:torch"}},
                  "result": {"item": D + "mine_lamp", "count": 2}},
    "ventilation_grate": {"type": "minecraft:crafting_shaped", "pattern": ["IGI", "GIG", "IGI"],
                          "key": {"I": {"item": "minecraft:iron_ingot"}, "G": {"item": D + "rusty_fence"}},
                          "result": {"item": D + "ventilation_grate", "count": 2}},
    "railway_ballast": {"type": "minecraft:crafting_shapeless",
                        "ingredients": [{"item": "minecraft:gravel"}, {"item": D + "slag"}],
                        "result": {"item": D + "railway_ballast", "count": 2}},
    "rail_sleepers": {"type": "minecraft:crafting_shaped", "pattern": ["L", "L"],
                      "key": {"L": {"item": D + "mine_timber_beam"}}, "result": {"item": D + "rail_sleepers", "count": 2}},
    "freight_wagon_plating": {"type": "minecraft:crafting_shaped", "pattern": ["RR", "RR"],
                              "key": {"R": {"item": D + "rusty_plate"}}, "result": {"item": D + "freight_wagon_plating", "count": 4}},
    "miners_ration": {"type": "minecraft:crafting_shapeless",
                      "ingredients": [{"item": "minecraft:bread"}, {"item": "minecraft:cooked_porkchop"}, {"item": "minecraft:beetroot"}],
                      "result": {"item": D + "miners_ration", "count": 1}},
    "iron_from_scrap": {"type": "minecraft:smelting", "ingredient": {"item": D + "iron_scrap"},
                        "result": "minecraft:iron_nugget", "experience": 0.05, "cookingtime": 100},
    "iron_from_scrap_blasting": {"type": "minecraft:blasting", "ingredient": {"item": D + "iron_scrap"},
                                 "result": "minecraft:iron_nugget", "experience": 0.05, "cookingtime": 50},
    "iron_from_gear": {"type": "minecraft:smelting", "ingredient": {"item": D + "rusty_gear"},
                       "result": "minecraft:iron_ingot", "experience": 0.3, "cookingtime": 200},
    "miners_token": {"type": "minecraft:crafting_shapeless",
                     "ingredients": [{"item": "minecraft:iron_nugget"}, {"item": "minecraft:iron_nugget"},
                                     {"item": "minecraft:gold_nugget"}],
                     "result": {"item": D + "miners_token", "count": 2}},
    "miners_pickaxe": {"type": "minecraft:crafting_shaped", "pattern": ["CAC", " S ", " S "],
                       "key": {"C": {"item": D + "coke"}, "A": {"item": D + "anthracite"},
                               "S": {"item": "minecraft:stick"}},
                       "result": {"item": D + "miners_pickaxe", "count": 1}},
    "donbass_ticket": {"type": "minecraft:crafting_shapeless",
                       "ingredients": [{"item": "minecraft:paper"}, {"item": "minecraft:coal"}, {"item": D + "miners_token"}],
                       "result": {"item": D + "donbass_ticket", "count": 1}},
}
