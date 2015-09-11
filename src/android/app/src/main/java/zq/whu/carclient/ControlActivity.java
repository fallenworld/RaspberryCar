package zq.whu.carclient;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;

import java.util.LinkedList;
import java.util.List;


public class ControlActivity extends ActionBarActivity {

    List<Button> buttons;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_control);
        NetUtil.init();
        buttons=new LinkedList<>();
        buttons.add((Button)findViewById(R.id.forward));
        buttons.add((Button)findViewById(R.id.backward));
        buttons.add((Button)findViewById(R.id.left));
        buttons.add((Button)findViewById(R.id.right));
        for (Button button : buttons) {
            button.setOnTouchListener(new View.OnTouchListener() {
                @Override
                public boolean onTouch(View v, MotionEvent event) {
                    if(event.getAction()==MotionEvent.ACTION_DOWN) {
                        switch(v.getId()) {
                            case R.id.forward:
                                NetUtil.sendMessage("w");
                                break;
                            case R.id.backward:
                                NetUtil.sendMessage("s");
                                break;
                            case R.id.left:
                                NetUtil.sendMessage("a");
                                break;
                            case R.id.right:
                                NetUtil.sendMessage("d");
                                break;
                            default:
                                break;
                        }
                    }
                    if(event.getAction()==MotionEvent.ACTION_UP) {
                        switch(v.getId()) {
                            case R.id.forward:
                                NetUtil.sendMessage("x");
                                break;
                            case R.id.backward:
                                NetUtil.sendMessage("t");
                                break;
                            case R.id.left:
                                NetUtil.sendMessage("b");
                                break;
                            case R.id.right:
                                NetUtil.sendMessage("e");
                                break;
                            default:
                                break;
                        }
                    }
                    return false;
                }
            });
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_control, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
