package com.toebarn.mobfind;

import java.util.Random;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitScheduler;

public class Main extends JavaPlugin implements Listener {
	@Override
	public void onEnable() {
		getLogger().info("Mobfind plugin initialized.");
		getServer().getPluginManager().registerEvents(this, this);
	}
	
	public boolean enabled = false;
	public Player player1 = null;
	public Player player2 = null;
	public int taskID;
	public int taskID2;
	public int time = 600;
	public String[] mobtypes = {"sheep","pig","cow","bat","cat","chicken","cod","donkey","fox","horse","mooshroom","parrot","rabbit","salmon","sheep","squid","tropical_fish","turtle","villager","creeper","drowned","guardian","husk","piglin","pillager","skeleton","zombie","zombie_villager","bee","dolphin","enderman","llama","spider","wolf","zombified_piglin"};
	public String mobtokill = "";
	public boolean successp1 = false;
	public boolean successp2 = false;
	public boolean single = false;
	public String startmessage;
	public String startmessage2;
	
	@EventHandler
    public void onMobDeath(EntityDeathEvent event) {
		if (enabled == true) {
			if(event.getEntity().getKiller() instanceof Player){
				final String mobtype = event.getEntityType().toString().toLowerCase().replace(' ', '_');
				final String mobtomatch = mobtokill.toLowerCase().replace(' ', '_');
				if (event.getEntity().getKiller() == player1) {
					if (mobtype.equals(mobtomatch)) {
						successp1 = true;
						getLogger().info("Player1 has completed their goal. ");
						Bukkit.broadcastMessage(ChatColor.GREEN+player1.getName()+" killed the right mob.");
						if (single == true) {
							Bukkit.broadcastMessage("Assigning new mob..."); 
							getLogger().info("New mob being assigned for the single player version of mobfind.");
							repeat1p(); 
							return;
						}
					}
				}
				if (event.getEntity().getKiller() == player2) {
					if (mobtype.equals(mobtomatch)) {
						successp2 = true;
						getLogger().info("Player2 has completed their goal. ");
						Bukkit.broadcastMessage(ChatColor.GREEN+player2.getName()+" killed the right mob. ");
					}
				}
				if (successp1 == true && successp2 == true) {
					player1.sendTitle(ChatColor.GREEN+"You both succeeded","Assigning a new mob...",10,40,10);
					player2.sendTitle(ChatColor.GREEN+"You both succeeded","Assigning a new mob...",10,40,10);
					repeat2p();
				}
			}
		}
	} 
	
	public void repeat1p() {
		getLogger().info("Restarting 1 player mobfind.");
		successp1 = false;
		Bukkit.getScheduler().cancelTask(taskID);
		mobfind1p();
	}
	
	public void repeat2p() {
		getLogger().info("Restarting 2 player mobfind.");
		successp1 = false;
		successp2 = false;
		mobtokill = "";
		Bukkit.getScheduler().cancelTask(taskID2);
		BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
		scheduler.scheduleSyncDelayedTask(this, new Runnable() {
    		// @Override this was not needed apparently
    		public void run() {
    			mobfind2p();
    		}
    	}, 80L);
	}
	
	public void mobfind1p() {
			time = 600;
			enabled = true;
			Random rand = new Random();
			final int mobindex = rand.nextInt(mobtypes.length)-1;
			mobtokill = mobtypes[mobindex];
			player1.sendMessage(ChatColor.GOLD+"You have to kill a "+mobtokill);
			BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
			taskID = scheduler.scheduleSyncRepeatingTask(this, new Runnable() {
				@SuppressWarnings("deprecation")
				public void run() {
					if(time > -1) {
						String subtitle = "";
						final int seconds = time % 60;
						final int minutes = (time - seconds) / 60;
						if (minutes >= 10 && seconds >= 10) {
							subtitle = Integer.toString(minutes) +":"+Integer.toString(seconds);
						}
						else if (minutes < 10 && seconds >= 10) {
							subtitle = "0"+Integer.toString(minutes) +":"+Integer.toString(seconds);
						}
						else if (minutes >= 10 && seconds < 10) {
							subtitle = Integer.toString(minutes) +":0"+Integer.toString(seconds);
						}
						else if (minutes < 10 && seconds <10) {
							subtitle = "0"+Integer.toString(minutes) +":0"+Integer.toString(seconds);
						}
						player1.sendTitle("",subtitle );
						time = time -1;
					}
					else if (time < 0){
						player1.sendMessage("You failed to kill the proper mob.");
						enabled = false;
						Bukkit.getScheduler().cancelTask(taskID);
					}
				}	
			}, 0L, 20L);
		} 
	
	public void mobfind2p() {
		time = 606;
		enabled = true;
		Random rand = new Random();
		final int mobindex = rand.nextInt(mobtypes.length)-1;
		mobtokill = mobtypes[mobindex];
		startmessage = ChatColor.GOLD + "You have to kill a ";
		startmessage2 = ChatColor.GOLD + mobtokill;
		BukkitScheduler scheduler = Bukkit.getServer().getScheduler();
		taskID2 = scheduler.scheduleSyncRepeatingTask(this, new Runnable() {
			@SuppressWarnings("deprecation")
			public void run() {
				if(time > -1) {
					String subtitle = "";
					final int seconds = time % 60;
					final int minutes = (time - seconds) / 60;
					if (minutes >= 10 && seconds >= 10) {
						subtitle = Integer.toString(minutes) +":"+Integer.toString(seconds);
					}
					else if (minutes < 10 && seconds >= 10) {
						subtitle = "0"+Integer.toString(minutes) +":"+Integer.toString(seconds);
					}
					else if (minutes >= 10 && seconds < 10) {
						subtitle = Integer.toString(minutes) +":0"+Integer.toString(seconds);
					}
					else if (minutes < 10 && seconds <10) {
						subtitle = "0"+Integer.toString(minutes) +":0"+Integer.toString(seconds);
					}
					if (time > 600) {
						player1.sendTitle(startmessage,startmessage2, 0, 20, 0 );
						player2.sendTitle(startmessage, startmessage2, 0, 20, 0);
					}
					else {
					player1.sendTitle("",subtitle );
					player2.sendTitle("", subtitle);
					}
					time = time -1;
				}
				else if (time < 0){
					if (successp1 == false && successp2 == false) {
						Bukkit.broadcastMessage(ChatColor.GOLD+"You both failed to kill the mob. Assigning a new one...");
						repeat2p();
					}
					else if (successp1 == true && successp2 == false){
						player1.sendTitle(ChatColor.GREEN+"You won the mobfind!","",10, 100,10);
						player2.sendTitle(ChatColor.RED+"You lost. Big oof.", "",10,100,10);
						enabled = false;
						Bukkit.getScheduler().cancelTask(taskID2);
					}
					else if (successp1 == false && successp2 == false) {
						player2.sendTitle(ChatColor.GREEN+"You won the mobfind!","",10, 100,10);
						player1.sendTitle(ChatColor.RED+"You lost. Big oof.", "",10,100,10);
						enabled = false;
						Bukkit.getScheduler().cancelTask(taskID2);
					}
				}
			}	
		}, 0L, 20L);
	}
	
	public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("startmobfind")) {
        	if (enabled == true) {
        		sender.sendMessage("There is an ongoing mobfind, so no.");
        		return false;
        	}
        	if (args.length==0) {
        		enabled = true;
        		single = true;
        		player1 = Bukkit.getPlayerExact(sender.getName());
        		mobfind1p();
        		return true;
        	}
        	else if (args.length == 1) {
        		enabled = true;
        		player1 = Bukkit.getPlayerExact(sender.getName());
        		player2 = Bukkit.getPlayerExact(args[0]);
        		if (sender.getName().equals(args[0])) {
        			sender.sendMessage("This version of mobfind is for testing purposes only.");
        		}
        		mobfind2p();
        		return true;
        	}
        	sender.sendMessage("Mobfind is a game only for two people");
        	return false;
        }
        else if (command.getName().equalsIgnoreCase("mobfindrules")) {
        	sender.sendMessage(ChatColor.AQUA + "Mobfind is a very simple game. \nYou will have ten minutes to hunt down the kind of mob that the game tells you to. \nIf both you and your friend cannot kill the mob in ten minutes, then you will both get another mob. \nIf you both kill your mob, you both move on to another mob. \nThe game will continue until one of you cannot kill a mob and the other can.");
        	return true;
        }
        return false;
	}
	
	@Override
	public void onDisable() {
		getLogger().info("Mobfind plugin closed.");
	}
}
