package master.iot.lo53lab;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private TextView mTextViewResult;
    private EditText serverIPWidget;
    private String macAddress;

    @SuppressLint("HardwareIds")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTextViewResult = findViewById(R.id.requestResult);
        serverIPWidget = findViewById(R.id.serverIP);

        WifiManager manager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        WifiInfo info = manager.getConnectionInfo();
        //macAddress = info.getMacAddress();
    macAddress = "B2:45:52:ED:1E:B8";
        mTextViewResult.setText(macAddress);


    }

    public void startCalibrationRequest(View view){
        String serverIp = String.valueOf(serverIPWidget.getText());
        if(serverIp.equals("")){
           // serverIp = "http://localhost:5000";
            /**
             * the address of the lost of emulator
             */
            serverIp = "http://10.0.2.2:5000";

        }
        double x=2;
        double y=2;
        double z=2;

        String url = serverIp + "/start_calibration?mac_addr=" + macAddress + "&x=" + x + "&y=" + y + "&z=" + z;
        sendRequest(url);
    }



    public void stopCalibrationRequest(View view){
        String serverIp = String.valueOf(serverIPWidget.getText());
        if(serverIp.equals("")){
            serverIp = "http://10.0.2.2:5000";
            // serverIp = "http://localhost:5000";

        }
        String url = serverIp + "/stop_calibration?mac_addr="+ macAddress ;
        sendRequest(url);
    }

    public void locateRequest(View view){
        String serverIp = String.valueOf(serverIPWidget.getText());
        if(serverIp.equals("")){
            serverIp = "http://10.0.2.2:5000";
            // serverIp = "http://localhost:5000";

        }


        String url = serverIp + "/locate?mac_addr="+ macAddress ;
        sendRequest(url);
    }

    private void sendRequest(String url) {

        showToast(url);

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(url)
                .build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {

                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {

                if (response.isSuccessful()) {
                    final String myResponse = response.body().string();
                    MainActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mTextViewResult.setText(myResponse);
                        }
                    });
                }
            }
        });
    }

    private void showToast(String url) {
        Context context = getApplicationContext();
        int duration = Toast.LENGTH_SHORT;

        Toast toast = Toast.makeText(context, url, duration);
        toast.show();
    }


}
