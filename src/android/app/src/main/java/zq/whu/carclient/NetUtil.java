package zq.whu.carclient;

import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.widget.Button;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

/**
 * Created by fallenworld on 2015/9/11.
 */
public class NetUtil {

    private static DatagramSocket udp;

    private static InetAddress address;

    private final static int PORT=9001;

    private static String ipAddress;

    //初始化
    public static void init() {
        try {
            udp=new DatagramSocket();
            address=InetAddress.getByName(ipAddress);
        }
        catch (SocketException e) {
            e.printStackTrace();
        }
        catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    //向小车端发送消息
    public static void sendMessage(final String key) {
        new Thread() {
            @Override
            public void run() {
                DatagramPacket packet=new DatagramPacket(key.getBytes(), key.getBytes().length, address, PORT);
                try {
                    udp.send(packet);
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();
    }

    public static void setIpAddress(String ipAddress) {
        NetUtil.ipAddress=ipAddress;
    }

}
