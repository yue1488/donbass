package com.donbass.mod;

import com.donbass.mod.registry.ModBlocks;
import com.donbass.mod.registry.ModCreativeTabs;
import com.donbass.mod.registry.ModFeatures;
import com.donbass.mod.registry.ModItems;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(DonbassMod.MOD_ID)
public class DonbassMod {
    public static final String MOD_ID = "donbass";

    public DonbassMod() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();

        // Blocks first: ModBlocks also queues the matching BlockItems into ModItems.ITEMS.
        ModBlocks.BLOCKS.register(modBus);
        ModItems.ITEMS.register(modBus);
        ModFeatures.FEATURES.register(modBus);
        ModCreativeTabs.TABS.register(modBus);
    }
}
