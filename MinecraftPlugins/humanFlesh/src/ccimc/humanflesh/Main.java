package ccimc.humanflesh;

import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.entity.EntityType;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;

public class Main extends JavaPlugin implements Listener {
	public static final String FLESH_ITEM_NAME = "Fresh Flesh";
	
	@Override
	public void onEnable() {
		getLogger().info("Jesus it works");
		getServer().getPluginManager().registerEvents(this, this);
	}
	
	@EventHandler
	public void onMobDeath(EntityDeathEvent event) {
		if (event.getEntity().getType() == EntityType.VILLAGER) {
			Location entityPosition = event.getEntity().getLocation();
			ItemStack drop = new ItemStack(Material.COOKED_CHICKEN, 1);
			ItemMeta meta = drop.getItemMeta();
			meta.setDisplayName(FLESH_ITEM_NAME);
			meta.setCustomModelData(1);
			drop.setItemMeta(meta);
			entityPosition.getWorld().dropItemNaturally(entityPosition, drop);
		}
	}
	
	@Override
	public void onDisable() {
		getLogger().info("No more flesh I guess...");
	}
}