using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;//use this namespace for sockets
using System.Net;//for ip addressing
using System.IO;//for streaming io
using System.Threading;//for running threads

namespace ChatClient
{
    //delegates are used to manipulate controls like text box and list box ....etc from threads, they are an interface.
    //we need this delegate to change the contents of the text box (received messages)
    delegate void UpdateTextBox(string msg);
    public partial class Form1 : Form
    {
        private TcpClient Client;//variable needed to listen for connections
        private BinaryReader MessageReader;//variable for reading messages
        private BinaryWriter MessageWriter;//variable for writing messages
        private NetworkStream DataStream;//variable for keeping server and client in a stream and synchronized
        private Thread ClientThread;//variable that is assigned to a thread listening for incoming connections and preventing the pc from blocking

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            //try if the ip address is written well 
            try
            {
                IPAddress.Parse(textBox3.Text);//
                ClientThread = new Thread(new ThreadStart(PerformConnection));
                ClientThread.Start();
            }
            catch (Exception)
            {
                MessageBox.Show("Wrong Ip Address");//signal the error in a message box
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //check if the their is a connection first
            try
            {
                if (Client.Connected)
                {
                    MessageWriter.Write(textBox2.Text);//send message via stream
                    textBox2.Clear();//clear text box after sending
                }
            }
            catch (Exception)
            {
                MessageBox.Show("no client is connected");//signal the error in a messagebox
            }
        }

        private void textBox2_KeyDown(object sender, KeyEventArgs e)
        {
            //if enter key was pressed
            if (e.KeyCode == Keys.Enter)
            {
                //check if the their is a connection first
                try
                {
                    if (Client.Connected)
                    {
                        MessageWriter.Write(textBox2.Text);//send message via stream
                        textBox2.Clear();//clear text box after sending
                    }
                }
                catch (Exception)
                {
                    MessageBox.Show("no client is connected");//signal the error in a messagebox
                }
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            System.Environment.Exit(System.Environment.ExitCode);//exit and close all threads and release all recources
        }

        //network functions used
        private void PerformConnection()
        {
            //try Connecting on the give ip address
            try
            {
                Client = new TcpClient();//assign new tcp client object
                ChangeTextBoxContent("Connecting......");
                Client.Connect(IPAddress.Parse(textBox3.Text), 80);//connect to given ip on port 80 allways
                DataStream = Client.GetStream();
                MessageReader = new BinaryReader(DataStream);
                MessageWriter = new BinaryWriter(DataStream);
                ChangeTextBoxContent("Connected");
                HandleConnection();
                MessageWriter.Close();
                MessageReader.Close();
                DataStream.Close();
                Client.Close();
            }
            catch (Exception)
            {
                MessageBox.Show("Unable to connect, wrong ip address");//signal the error in a message box
            }
        }
        private void HandleConnection()
        {
            string message;
            //loop until infinity
            do
            {
                //try reading from the data stream if anything went wrong with the connection break
                try
                {
                    message = MessageReader.ReadString();//read message
                    ChangeTextBoxContent(message);//call the function that manipulates text box from a thread and change the contents.
                }
                catch (Exception)
                {
                    ChangeTextBoxContent("connection Lost");
                    break;//get out of the while loop
                }
            } while (true);
        }
        private void ChangeTextBoxContent(string tx)
        {
            if (textBox1.InvokeRequired)//if the messages text box needs a delegate invoking
            {
                Invoke(new UpdateTextBox(ChangeTextBoxContent), new object[] { tx });
            }
            else
            {
                //if no invoking required then change
                textBox1.Text += tx + "\r\n";//concatinate the original with the given message and a new line
            }
        }
    }
}
