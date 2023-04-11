using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using System.Threading.Tasks;

public class DesktopForm : Form {
    public TextBox WSLText; 
    public TransparentControl foreground_image;

    public DesktopForm() {
        // this.Size = new Size(1920, 1080);
        this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
        Int32 width = this.Width;
        Int32 height = this.Height;
        double widthRatio = ((double) width) / ((double) 1920);
        double heightRatio = ((double) height) / ((double) 1080); 
        // this.FormBorderStyle = FormBorderStyle.FixedSingle; 
        this.foreground_image = new TransparentControl();
        this.foreground_image.Size = new Size(width, height);
        this.foreground_image.Image = resizeImage(Image.FromFile(@".\linuxTerminalWallpaper.png"), new Size(width, height));
        this.WSLText = new TextBox(); 
        this.WSLText.AutoSize = false;
        this.WSLText.Location = new Point((Int32)(827 * widthRatio), (Int32)(514 * heightRatio));
        this.WSLText.Size = new Size((Int32)(311 * widthRatio), (Int32)(189 * heightRatio)); 
        this.WSLText.BackColor = System.Drawing.ColorTranslator.FromHtml("#000000");
        this.WSLText.ForeColor =  System.Drawing.ColorTranslator.FromHtml("#00ff00");
        this.WSLText.Padding = new Padding(8);
        this.WSLText.Multiline = true;
        this.WSLText.WordWrap = true; 
        this.WSLText.AcceptsTab = true; 
        this.WSLText.AcceptsReturn = true;
        this.WSLText.ReadOnly = true; 
        this.WSLText.Font = new Font("Terminal", 11);
        this.Controls.Add(foreground_image); 
        this.Controls.Add(this.WSLText); 
        this.WSLText.SendToBack(); 
    }

    public static Image resizeImage(Image imgToResize, Size size) {
        return (Image)(new Bitmap(imgToResize, size));
    }

    [STAThread]
    static void Main(){
        Application.EnableVisualStyles();
        DesktopForm formInstance = new DesktopForm(); 
        Task.Run(() => formInstance.cycleText());
        // Task<int> cycleTask = formInstance.cycleText(); 
        Application.Run(formInstance);
    }

    private async Task<int> cycleText() {
        while (true) {
            genericDisplay("Welcome to WSLDesktop!"+Environment.NewLine+" Click to Launch Window", 50);
            await Task.Delay(TimeSpan.FromSeconds(2));
            int amountOfOptions = 2;
            int randomChoice = chooseRandomNumber(1, amountOfOptions);
            switch (randomChoice) {
                case 1:
                    genericDisplay("~# whoami"+Environment.NewLine+"root"+Environment.NewLine+"~# ls"+Environment.NewLine+".ssh  config.txt  rockyou.txt"+Environment.NewLine+"~# cd .ssh"+Environment.NewLine+"~/.ssh # exit", 50); 
                    await Task.Delay(TimeSpan.FromSeconds(2));
                    break; 
                case 2: 
                    genericDisplay("~# sudo apt update"+Environment.NewLine+"Get:1 http://security.ubuntu.com/ubuntu focal/universe amd64 [698 kB]"+Environment.NewLine+"Fetched 698 kB in 1s (698 kB/s)"+Environment.NewLine+"Reading package lists... Done"+Environment.NewLine+"Building dependency tree"+Environment.NewLine+"Reading state information... Done"+Environment.NewLine+"22 packages can be upgraded. Run 'apt list --upgradable' to see them.", 20);
                    await Task.Delay(TimeSpan.FromSeconds(2));
                    break; 
            }
        }
    }
    
    private void genericDisplay(String message, int delayTime) {
        setScreenText(" ");
        this.ActiveControl = this.foreground_image;
        foreach (char c in message) {
            appendScreenText(c);
            Task.Delay(TimeSpan.FromMilliseconds(delayTime)).Wait();
        }
    }

    // private void setScreenText(String str) {
    // WSLText.Text = str;
    // }

    private void appendScreenText(char ch) {
        WSLText.AppendText(ch.ToString()); 
    }

    private void setScreenText(String text){  
        if(InvokeRequired) {  
            this.Invoke((MethodInvoker) delegate() { setScreenText(text); });  
            return;  
        }  
        WSLText.Text = text;  
        this.foreground_image.Redraw(); 
    } 
    
    private int chooseRandomNumber(int lowest, int highest) {
        Random rand = new Random(); 
        double randValue = rand.NextDouble(); 
        return (Int32) Math.Floor(randValue * (highest - lowest + 1)) + lowest;
    }
}