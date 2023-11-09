// This is my first plug-in. For basic plug-in information, 
// review this video: https://www.youtube.com/watch?v=-LPBsw5qM-I

package com.toebarn.MCplugin;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitScheduler;
import java.util.Random;

public class Main extends JavaPlugin implements Listener{
	
	@Override
	public void onEnable() {
		getServer().getPluginManager().registerEvents(this, this);
	    getLogger().info("Mobhunt plugin initialized.");
	    
	}
	
	public boolean enabled = false;
	public int time;
	public int taskID;
	public Player player1;
	public Player player2; 
	
	@EventHandler
    public void onMobDeath(EntityDeathEvent event) {
		if (enabled == true) {
			if(event.getEntity().getKiller() instanceof Entity || event.getEntity().getKiller() instanceof Player){
				final String mobtype = event.getEntityType().toString();
				getLogger().info(event.getEntity().getKiller().getName()+" killed a "+mobtype);
				final String mobegg = mobtype.toLowerCase().replace(" ","_");
				final String mobeggcommand = "give " + event.getEntity().getKiller().getName()+" "+mobegg+"_spawn_egg";
				Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),mobeggcommand);
			}
		}
	} 
	
	@EventHandler
	public void onPlayerDeath(PlayerDeathEvent event){
		if (enabled == true) {
			Player onewhodied = event.getEntity();
			Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"worldborder set 30000000");
			getLogger().info("The player <"+onewhodied.getName()+"> died.");
			if (onewhodied == player1) {
				Bukkit.broadcastMessage(ChatColor.GREEN + "The Winner of MobHunt is "+player2.getName());
			}
			else if (onewhodied == player1) {
				Bukkit.broadcastMessage(ChatColor.GREEN + "The Winner of MobHunt is "+player2.getName());
			}
			stopTimer();
			enabled = false;
			Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "op conifer0us");
		}
	}
	
	public void setTimer(int amount) {
        time = amount;
    }
	
	public void startTimer() {
        BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
        taskID = scheduler.scheduleSyncRepeatingTask(this, new Runnable() {
            @Override
            public void run() {
            	if(time == 0) {
                    Bukkit.broadcastMessage(ChatColor.RED + "Time is up!");
                    stopTimer();
                    final String command3 = "launch "+player1.getName();
                    final String command4 = "launch "+player2.getName();
                    final String command5 = "tp "+player1.getName()+" 0 71 0";
                    final String command6 = "tp "+player2.getName()+"0 71 0";
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command3);
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command4);
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command5);
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command6);
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "worldborder center 0 0");
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"worldborder set 100");
                    Bukkit.broadcastMessage(player1.getName() +" and " +player2.getName()+" are facing off in mobhunt. Who will prevail?");
                    return;
                }
            	if(time % 300 == 0) {
                    Bukkit.broadcastMessage(ChatColor.RED + "Time remaining: " + time/60 + " minutes");
                }
            	time = time -1;
            }
        }, 0L, 20L);
    }
	
	public void stopTimer() {
        Bukkit.getScheduler().cancelTask(taskID);
    }
	
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("startmobhunt")) {
        	for (String argument : args) {
        		if (Bukkit.getPlayerExact(argument)==null) {
        			if (args[0] == argument || args[1] == argument) {
        				sender.sendMessage("One or more of the usernames entered are not valid.");
        				return false;
        			}
        		}
        	}
        	if (args.length > 2 || args.length == 0) {
        		sender.sendMessage("Only works on two people");
        		return false;
        	}
        	if (args.length == 1) {
        		player2 = Bukkit.getPlayerExact(args[0]);
        		String executor = ((Player) sender).getName();
        		player1 = Bukkit.getPlayerExact(executor);
        		if (player1 == player2) {
        			sender.sendMessage("Mobhunt only works normally with 2 people, but this will work for testing.");
        		}
            }
        	else if (args.length == 2) {
        		player1 = Bukkit.getPlayerExact(args[0]);
        		player2 = Bukkit.getPlayerExact(args[1]);
        		if (player1 == player2) {
        			sender.sendMessage("Mobhunt only works with 2 people.");
        			return false;
        		}
        	}
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "deop "+player1.getName());
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"deop "+player2.getName());
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "advancement revoke "+player1.getName()+" everything");
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "advancement revoke "+player2.getName()+" everything");
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "gamemode survival "+player1.getName());
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "gamemode survival "+player2.getName());
        	enabled = true;
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"time set day");
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"gamerule doDaylightCycle true");
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"weather clear");
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),"gamerule doWeatherCycle true");
        	player1.sendMessage("Welcome to Minecraft Mobhunt! Thank you for participating you are truly a legend. If are confused at any point, type /mobhuntrules. ");
        	player2.sendMessage("Welcome to Minecraft Mobhunt! Thank you for participating you are truly a legend. If are confused at any point, type /mobhuntrules. ");
        	Random rand = new Random();
        	int coord1 = rand.nextInt(40000)-20000;
        	int coord2 = rand.nextInt(40000)-20000;
        	int coord3 = rand.nextInt(40000)-20000;
        	int coord4 = rand.nextInt(40000)-20000;
        	final World world = player1.getWorld();
        	String command1 = "tp "+player1.getName()+" "+Integer.toString(coord1)+" 750 "+Integer.toString(coord2);
        	String command2 = "tp "+player2.getName()+" "+Integer.toString(coord3)+" 750 "+Integer.toString(coord4);
        	BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
        	Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command1);
            Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(),command2);
        	world.getBlockAt(coord1,225,coord2).setType(Material.WATER);
        	world.getBlockAt(coord3,225,coord4).setType(Material.WATER);
            getLogger().info("Waiting before replacing water...");
        	scheduler.scheduleSyncDelayedTask(this, new Runnable() {
        		// @Override this was not needed apparently
        		public void run() {
        			world.getBlockAt(coord1,225,coord2).setType(Material.AIR);
                	world.getBlockAt(coord3,225,coord4).setType(Material.AIR);
                	getLogger().info("Water has been removed. Players floating safely down to respective locations.");
        		}
        	}, 300L);
        	setTimer(3600);
        	startTimer();
        	return true;
        }
        else if (command.getName().equalsIgnoreCase("mobhuntrules")){
        	sender.sendMessage(ChatColor.AQUA+"Mobhunt is a very simple game. For 60 minutes, you and your friend will be apart on the map in survival mode. \n\nIn this time, gather gear or whatever you want to do. Every mob you kill will drop its spawn egg. \n\nWhen the 60 minutes are up, you will be teleported to the center of the map with a worldborder of 100 blocks. \n\nYour goal is to then kill each other, not with pvp but with the spawn eggs you collected. \n\nYou will be able to kill more mobs after 60 minutes and collect their eggs, so don't worry about running out of eggs once teleported. \n\nAsk someone with console permissions to run /stopmobhunt to stop a running mobhunt.");
        	return true;
        }
        else if (command.getName().equalsIgnoreCase("stopmobhunt")) {
        	if (enabled == true) {
        		stopTimer();
        		enabled = false;
        		player1.sendMessage(ChatColor.RED +"Mobhunt has been stopped.");
        		player2.sendMessage(ChatColor.RED+"Mobhunt has been stopped.");
        		Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), "op conifer0us");
        		player1 = null;
        		player2 = null;
        		return true;
        	}
        }	
        return false;
	}
	
	@Override
	public void onDisable() {
		
	    getLogger().info("Mobhunt plugin closed.");
	    
	}
	
	
}