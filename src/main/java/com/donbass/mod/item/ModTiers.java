package com.donbass.mod.item;

import com.donbass.mod.registry.ModItems;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraftforge.common.ForgeTier;

/** Tool tiers added by the mod. */
public final class ModTiers {
    /**
     * Miner's pickaxe: iron-level mining, a bit more durable and faster than iron,
     * repaired with anthracite. The ingredient is resolved lazily because items
     * are not registered yet when this class is loaded.
     */
    public static final Tier MINER = new ForgeTier(2, 650, 6.5F, 2.0F, 14,
            BlockTags.NEEDS_IRON_TOOL, () -> Ingredient.of(ModItems.ANTHRACITE.get()));

    private ModTiers() {}
}
