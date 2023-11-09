package com.toebarn.basiccommands;

import java.util.Random;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.Listener;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitScheduler;
import org.bukkit.util.Vector;

public class Main extends JavaPlugin implements Listener {
	@Override
	public void onEnable() {
		getLogger().info("Basic command plugin initialized.");
	}
	
	public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("launch")) {
        	if (args.length == 1) {
        		if (Bukkit.getPlayerExact(args[0]) == null) {
        			sender.sendMessage("The player that you selected does not exist or is not currently on the server.");
        			return false;
        		}
            sender.sendMessage("Launching "+args[0]);
            Random rand = new Random();
            final int horizontal = rand.nextInt(200)-100;
            final double split = rand.nextDouble();
            Player p = Bukkit.getPlayer(args[0]);
            p.setVelocity(p.getVelocity().add(new Vector(split * horizontal, 100, (split-1)*horizontal)));
        	return true;
        	}
        	else if (args.length == 0) {
        		sender.sendMessage("Launching "+sender.getName());
        		Random rand = new Random();
        		final int horizontal = rand.nextInt(200)-100;
        		final double split = rand.nextDouble();
        		Player p = Bukkit.getPlayer(sender.getName());
        		p.setVelocity(p.getVelocity().add(new Vector(split * horizontal, 100, (split-1)*horizontal)));
        		return true;
        	}
        	sender.sendMessage("Launch command works on exactly one player");
        	return false;
        }
        else if (command.getName().equalsIgnoreCase("heal")) {
        	if (args.length == 0) {
        		Player playertoheal = Bukkit.getPlayerExact(sender.getName());
        		playertoheal.setHealth(20.0);
        		playertoheal.setFoodLevel(20);
        		sender.sendMessage(ChatColor.GOLD+"Healed "+playertoheal.getName());
        		return true;
        	}
        	else if (args.length==1) {
        		Player playertoheal = Bukkit.getPlayerExact(args[0]);
        		playertoheal.setHealth(20.0);
        		playertoheal.setFoodLevel(20);
        		sender.sendMessage(ChatColor.GOLD+"Healed "+playertoheal.getName());
        		return true;
        	}
        }
        else if (command.getName().equalsIgnoreCase("hea")) {
        	((Player) sender).sendTitle(ChatColor.LIGHT_PURPLE+"DERPY DERP", "Derp Derp Derp", 20, 100, 20);
        	BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
        	scheduler.scheduleSyncDelayedTask(this, new Runnable() {
        		// @Override this was not needed apparently
        		public void run() {
        			Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"kick "+sender.getName()+" You are a massive DERP hahaha typos are for losers lool");
        		}
        	}, 300L);
        }
        else if (command.getName().equalsIgnoreCase("clearitems")) {
        	Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "kill @e[type=item]");
        	return true;
        }
        return false;
	}
	
	@Override
	public void onDisable() {
		getLogger().info("Basic command plugin closed.");
	}
}
