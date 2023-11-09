package toebarn.com.mobChaos;

import java.util.Random;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.EntityType;
import org.bukkit.entity.Fireball;
import org.bukkit.entity.Ghast;
import org.bukkit.entity.LargeFireball;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.ProjectileLaunchEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitScheduler;
import org.bukkit.util.Vector;

public class Main extends JavaPlugin implements Listener{
	
	public boolean mobchaos = false;
	private int taskID = 0;
	private int taskID2 = 0;
	public double timeleft = 1.0;
	public Vector playerposition;
	public Vector mobposition;
	public Vector difference;
	Random r = new Random();
	public boolean chaos() {
		return mobchaos;
	}
	
	@Override
	public void onEnable() {
		getLogger().info("Mobfind plugin initialized.");
		getServer().getPluginManager().registerEvents(this, this);
	}
	
	public void mobattraction(Player runner) {
		getLogger().info(runner.getName()+" is attracting mobs now.");
		BukkitScheduler scheduler1 = Bukkit.getServer().getScheduler();
		taskID2 = scheduler1.scheduleSyncRepeatingTask(this, new Runnable() {
			public void run() {
				if (chaos()) {
					for (Entity e : runner.getWorld().getEntities()) {
						mobposition = e.getLocation().toVector();
						playerposition = runner.getLocation().toVector();
						if (!(e instanceof Player) && !(e instanceof Fireball)) {
							difference = new Vector(0,0,0);
							double x1 = playerposition.getX();
							double x2 = mobposition.getX();
							double y1 = playerposition.getY();
							double y2 = mobposition.getY();
							double z1 = playerposition.getZ();
							double z2 = mobposition.getZ();
							difference.setX(x1-x2);
							difference.setY(y1-y2);
							difference.setZ(z1-z2);
							difference = difference.multiply(.01);
							e.setVelocity(difference);
						}
					}
				}
			}
		}, 0L, 1L);
	}
	
	@EventHandler
	public void onGhastFire(ProjectileLaunchEvent event){
        if(chaos() && taskID == 0 && event.getEntity().getShooter() instanceof Ghast){
        	int i = 0;
			while (i < 700){
				double x = r.nextDouble() * 10 - 5;
				double y = r.nextDouble() * 10 - 5;
				double z = r.nextDouble() * 10 - 5;
				final LargeFireball a = (LargeFireball) event.getEntity().getWorld().spawnEntity(event.getEntity().getLocation().add(x,y,z),EntityType.FIREBALL);
				a.setVelocity(new Vector(5*x, 5*y, 5*z));
				i++;
			}
        }
	}
	
	public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
		if (command.getName().equalsIgnoreCase("togglechaos")) {
			if (mobchaos == false) {
				mobchaos = true;
				mobattraction((Player) sender);
			} else {
				mobchaos = false;
				Bukkit.getServer().getScheduler().cancelTask(taskID2);
				Bukkit.getServer().getScheduler().cancelTask(taskID);
				taskID = 0;
				taskID2 = 0;
			}
			return true;
		}
		return false;
	}
	
	@Override
	public void onDisable() {
		getLogger().info("Mobfind plugin closed.");
	}
}
