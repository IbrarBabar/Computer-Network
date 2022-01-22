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

namespace ChatServer
{
    //delegates are used to manipulate controls like text box and list box ....etc from threads, they are an interface.
    //we need this delegate to change the contents of the text box (received messages)
    delegate void UpdateTextBox(string msg);
    public partial class Form1 : Form
    {
        private TcpListener ConnectionListener;//variable needed to listen for connections
        private BinaryReader MessageReader;//variable for reading messages
        private BinaryWriter MessageWriter;//variable for writing messages
        private Socket ClientConnection;//variable for holding the client connection
        private NetworkStream DataStream;//variable for keeping server and client in a stream and synchronized
        private Thread ListeningThread;//variable that is assigned to a thread listening for incoming connections and preventing the pc from blocking

        public Form1()//constructor
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)//when form is loading
        {
        }

        private void button1_Click(object sender, EventArgs e)//connect and listen button
        {
            //try if the ip address is written well 
            try
            {
                IPAddress.Parse(textBox3.Text);//
                ListeningThread = new Thread(new ThreadStart(ListenForConnections));//assign thread variable with the blocking function
                ListeningThread.Start();//start the thread that will wait for connections
            }
            catch (Exception)
            {
                MessageBox.Show("Wrong Ip Address");//signal the error in a message box
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //check if the their is a client first
            try
            {
                if (ClientConnection.Connected)
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
            if (e.KeyCode == Keys.Enter)//check if enter key was pressed
            {
                //check if the their is a client first
                try
                {
                    if (ClientConnection.Connected)
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

        //functions used for networks
        private void ListenForConnections()
        {
            //try listening with the given ip address
            try
            {
                ConnectionListener = new TcpListener(IPAddress.Parse(textBox3.Text), 80);//listen to given ip on port 80 allways
                ConnectionListener.Start();//start listening;
                ChangeTextBoxContent("Listening For Connections");
                ClientConnection = ConnectionListener.AcceptSocket();//wait untill client connects (blocking function) if connected return a socket 
                DataStream = new NetworkStream(ClientConnection);//initialize a stream 
                MessageReader = new BinaryReader(DataStream);//use reader within the stream
                MessageWriter = new BinaryWriter(DataStream);//use writer within the stream
                ChangeTextBoxContent("Connection Received");
                HandleConnection();//handle the reading and writing 
                //here the client disconnected or something went wrong with the connection
                MessageReader.Close();//close the reader;
                MessageWriter.Close();//close the writer;
                DataStream.Close();//close the stream;
                ClientConnection.Close();//close thre connection
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
