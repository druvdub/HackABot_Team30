#include <MsTimer2.h>

// Basic test of Mona robot including proximity sensors and open-loop motion control

// pin config for basic platform test
// Motors
int Motor_right_PWM = 10;  //   0 (min speed) - 255 (max speed) 
int Motor_right_direction = 5;  //   0 Forward - 1 Reverse
int Motor_left_PWM = 9;    //   0 (min speed) - 255 (max speed)  
int Motor_left_direction = 6;   //   0 Forward - 1 Reverse
#define Forward 0
#define Reverse 1

// LED
int LED1 = 13;
int LED2 = 12;
int IR_enable = 4;
int IR_threshold = 900; // 0 white close obstacle -- 1023 no obstacle

int Left_forward_speed = 50;
int Right_forward_speed = 50;

// environment variables stored by the bot
int x_arena_size = 0, y_arena_size = 0;
int cur_x_coord = 0, cur_y_coord = 0;
int prev_x_coord = 0, prev_y_coord = 0;
int cur_angle = 0, pre_angle = 0;


int ball_x = 0, ball_y = 0;
int goal_1_x = 0, goal_1_y = 0;
int goal_2_x = 0, goal_2_y = 0;

// TODO: Adjust angle range to be 0-360 see functions below to change
// charge_ball

bool transmission_setup_done = false;

// utility functions
float dot(float vec_1, float vec_2) {
	return vec_1[0]*vec_2[0] + vec_1[1]*vec_2[1] + vec_1[2]*vec_2[2];	
}

float magnitude(float vec_1) {
	float base;
	base = vec_1[0]*vec_1[0] + vec_1[1]*vec_1[1] + vec[2]*vec_1[2];
	return pow(base, 0.5);
}


void setup() {
// initialize serial communication at 9600 bits per second:
 Serial.begin(9600);

// TODO: Init connection with the transmittor
// May be a loop waiting to make a connection...

// Obtain the values like the size of the arena, current values of the bots and the ball,
	
// Find the coordinates where to make a goal 
// Obtain initial coordinates of the bot which should be set to cur coords 
// Determine out side of the arena 

// initialize Ports
  pinMode(Motor_left_PWM, OUTPUT);
  pinMode(Motor_right_PWM, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(IR_enable, OUTPUT);
}

// movement functions
void forward(){
  analogWrite(Motor_right_PWM, Right_forward_speed); // right motor
  digitalWrite(Motor_right_direction, Forward); //right
  analogWrite(Motor_left_PWM, Left_forward_speed); // left 
  digitalWrite(Motor_left_direction, Forward); //left
}

void reverse(int delay_time){
  analogWrite(Motor_right_PWM, 120); // right motor
  digitalWrite(Motor_right_direction, Reverse); //right
  analogWrite(Motor_left_PWM, 120); // left 
  digitalWrite(Motor_left_direction, Reverse); //left
  delay(delay_time);
}

void right(int delay_time){
  reverse(50);
  analogWrite(Motor_right_PWM, 150); // right motor
  digitalWrite(Motor_right_direction, Reverse); //right
  analogWrite(Motor_left_PWM, 40); // left 
  digitalWrite(Motor_left_direction, Forward); //left
  delay(delay_time);
}

void left(int delay_time){
  reverse(50);
  analogWrite(Motor_right_PWM, 40); // right motor
  digitalWrite(Motor_right_direction,Forward); //right
  analogWrite(Motor_left_PWM, 150); // left 
  digitalWrite(Motor_left_direction,Reverse); //left
  delay(delay_time);
}

// Variables for 5 IR proximity sensors 
int IR_right,IR_right_front,IR_front,IR_left_front,IR_left;

void IR_proximity_read(){    // read IR sensors 
  int n=5;  // average parameter
  digitalWrite(IR_enable, HIGH);  //IR Enable
  IR_right=0;
  IR_right_front=0;
  IR_front=0;
  IR_left_front=0;
  IR_left=0;
  for (int i=0;i<n;i++){
    IR_right+=analogRead(A3);
    IR_right_front+=analogRead(A2);
    IR_front+=analogRead(A1);
    IR_left_front+=analogRead(A0);
    IR_left+=analogRead(A7);
    delay(5);
  }
  IR_right/=n;
  IR_right_front/=n;
  IR_front/=n;
  IR_left_front/=n;
  IR_left/=n; 
}

// obstacle avoidance
void Obstacle_avoidance(){
  if (IR_front<IR_threshold){
      digitalWrite(LED2,HIGH);
      reverse(300);
      right(500);
      digitalWrite(LED2,LOW);
  }
  if (IR_right<IR_threshold || IR_right_front<IR_threshold){
      digitalWrite(LED2,HIGH);
      right(500);
      digitalWrite(LED2,LOW);
  } else {
      if (IR_left<IR_threshold || IR_left_front<IR_threshold){
          digitalWrite(LED2,HIGH);
          left(500);
          digitalWrite(LED2,LOW);
      } else forward();
  } 
}

// send IR readings to Serial Monitor
void Send_sensor_readings(){
 Serial.print(IR_right);
 Serial.print(',');
 Serial.print(IR_right_front);
 Serial.print(',');
 Serial.print(IR_front);
 Serial.print(',');
 Serial.print(IR_left_front);
 Serial.print(',');
 Serial.println(IR_left);  
}

bool rotation_direction(int point_x, int point_y) {
	// return True for clockwise
	// or False for anticlockwise
	
	
	
	
}

float bot_orientation_to_point(int point_x, int point_y) {
	float temp;
	float r_diff[2] = {0,0};
	float rotation[3] = {0,0,0,0,0,0};
	// R r
	float theta = abs(cur_angle - atan(cur_y_coord/cur_x_coord));
	float R[2] = {cos(theta) * cur_x_coord - sin(theta) *  cur_y_coord, 
				sin(theta) * cur_x_coord + cos(theta) * cur_y_coord};
	// r2 - r1
	r_diff[0] = point_x - cur_x_coord;
	r_diff[1] = point_x - cur_y_coord;
	// R r dot (r2 - r1)
	temp = dot(R,r_diff);
	return acos((magnitude(R) * magnitude(r_diff))/temp)
	// magnitude
}

void charge_ball() {
	// check where the ball is position the bot to face it
		
	//int ball_x = 0, ball_y = 0
	// 

}

bool stuck_check() {
	if abs(cur_x_coord - prev_x_coord) + abs(cur_y_coord - prev_y_coord) >= 0.0 {
		// stuck
		return True;
	} else {
		return False;
	}
}

void find_velocities_and_directions(){
  // this functions should find the velocities and directions of the attacking bot 

  // Cases to be considered: 
  // 1. When the prev and cur coords are not different much which may indicate a collision with 
  // another player's bot
  // 2. Going towards the ball - it would be useful to put the max speed possible for the bot to push 
  // 3. When the ball is in our side, then it could try to push towards opponent's side? 
  // 4. When the bot is near the wall (it can be calculated mathematically when it is the case)
  // 5.   
}

void Stop(){ // set speeds to 0
  analogWrite(Motor_right_PWM, 0); // right motor
  analogWrite(Motor_left_PWM, 0); // left 
  MsTimer2::start();
}

// the loop routine runs over and over again forever:
void loop() {
  // TODO: get data from the transmittor 


  digitalWrite(LED1,HIGH); //Top LED
  IR_proximity_read();
  Send_sensor_readings(); 
  Obstacle_avoidance();
  digitalWrite(LED1,LOW); //Top LED

  // TODO: Update prev coords 


  delay(100);        // delay in between reads for stability
}
