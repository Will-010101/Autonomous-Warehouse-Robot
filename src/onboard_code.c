#include <16F1937.h>
#device ADC=10
#use delay(internal=32MHz)
#fuses MCLR,NOWDT
#use rs232(baud=9600,parity=N,xmit=PIN_C6,rcv=PIN_C7,bits=8,stream=PORT1)
#use i2c(master,sda=PIN_c4,scl=PIN_c3)

#define Rkey      InPut(PIN_B4)        //Right Key
#define Lkey      InPut(PIN_B5)        //Left Key

#define LED1_high   OutPut_high(PIN_C5)
#define LED1_low    OutPut_low(PIN_C5)
#define LED2_high   OutPut_high(PIN_D5)
#define LED2_low    OutPut_low(PIN_D5)
#define LED3_high   OutPut_high(PIN_D6)
#define LED3_low    OutPut_low(PIN_D6)
#define LED4_high   OutPut_high(PIN_D7)
#define LED4_low    OutPut_low(PIN_D7)

#define LED1_toggle   OutPut_toggle(PIN_C5)
#define LED2_toggle   OutPut_toggle(PIN_D5)
#define LED3_toggle   OutPut_toggle(PIN_D6)
#define LED4_toggle   OutPut_toggle(PIN_D7)

#define IN1_high  OutPut_high(PIN_D0)
#define IN2_high  OutPut_high(PIN_D1)
#define IN3_high  OutPut_high(PIN_D2)
#define IN4_high  OutPut_high(PIN_A6)
#define IN1_LOW   OutPut_LOW(PIN_D0)
#define IN2_LOW   OutPut_LOW(PIN_D1)
#define IN3_LOW   OutPut_LOW(PIN_D2)
#define IN4_LOW   OutPut_LOW(PIN_A6)

//!#define maxspeed 700   //max=1023
//kp=7.5(150/20)

unsigned int1 cal_done=0,start=0;
unsigned int16 pr=0, angle=400  ;
signed int16 gyro_value=550,error;
float maxspeed;

int8 data[4];
signed int16 z;

int flg_gripper=0;
float dis=1000;
char imput;
unsigned int16 count_start=0,angle2=0,x1=100,x2=100,x3=100,count_sg90_open=0,count_sg90_close=0,count_sg90_back=0;

#int_rda
void input_data_bluetooth()
{
   imput=getchar();
   if(count_start==0 && imput=='*') {count_start=1; angle2=0;}
   else if(count_start==1 && imput!='*'){x1=(imput-'0'); count_start=2;  }
   else if(count_start==2 && imput!='*'){x2=(imput-'0'); count_start=3;  }
   else if(count_start==2 && imput=='*'){count_start=0; angle=x1;}
   else if(count_start==3 && imput!='*'){x3=(imput-'0'); count_start=4; }
   else if(count_start==3 && imput=='*'){count_start=0; angle=(x1*10)+x2;}
   else if(count_start==4 && imput=='*'){count_start=0; angle=(x1*100)+(x2*10)+x3;}
   
}

VOID motorspeed(signed int16 Left_velocity,signed int16 Right_velocity)
{
   IN1_high; IN2_low; IN3_high; IN4_low;
   
   if(Left_velocity>300){Left_velocity=300;}
   if(Left_velocity<-300){Left_velocity=-300;}
   if(Right_velocity>300){Right_velocity=300;}
   if(Right_velocity<-300){Right_velocity=-300;}
   if(Left_velocity<=0)
   {
      if(Left_velocity==0 )//stop mode
      {
         IN1_low;IN2_low; left_velocity=1;
      }
      else {IN1_low; IN2_high; Left_velocity*=-1;}   
   }   
   
   if(Right_velocity<=0)
      {
         if(Right_velocity==0 )//stop mode
         {
            IN3_low;IN4_low; Right_velocity=1;
         }
         else {IN3_low; IN4_high; Right_velocity*=-1;}   
      }   
    
    set_pwm1_duty((signed int16)Left_velocity);
    set_pwm2_duty((signed int16)Right_velocity);   
}

unsigned int8 get_ack_status(unsigned int8 address)
{
   unsigned int8 status;
   
   i2c_start();
   status = i2c_write(address); 
   i2c_stop();
    
   if(status==0)  return(TRUE);
   else           return(FALSE);
}

void Search_i2c()
{
   unsigned int8 status;
   //printf("\n\rStart:\n\r");
   delay_ms(1000);
   unsigned int8 count = 0;
   for(unsigned int8 i=0x10; i < 0xF0; i+=2) 
   { 
    status = get_ack_status(i); 
    if(status == TRUE) 
      {  
         //printf("Addr:%X\n",i);
         count++; 
         delay_ms(500); 
      } 
   } 
   //if(count == 0)  //printf("Nothing Found\n"); 
   //else            //printf("Chips Found=%u\n",count); 
}

void set_gyro_zero()
{
//for set Z zero just call ones /Satyar
       // delay_us(10000);
        delay_us(10000);
        i2c_start();
        i2c_write(0x24);
        i2c_write(0x00);
        i2c_stop();
        delay_us(10000);
}

signed int16 get_gyro_data(void)
{
      //for get angel from Z Call /Satyar
      i2c_start();
      i2c_write(0x25);
      data[0]=i2c_read();
      data[1]=i2c_read();
      data[2]=i2c_read();
      data[3]=i2c_read(0);
      i2c_stop();
      z=( (signed int16) make16(data[1],data[0]) );
      return z;
     // x=( (signed int16) make16(data[3],data[2]) );
}

#INT_TIMER1
void t1_isr()
{
  pr++;
}

void sg90_open()
{

   for(int i=0;i<2;i++)
         {
         output_high(pin_a2);
         delay_us(18000);
         output_low(pin_a2);
         delay_us(2000);
         }

   
}
void sg90_close()
{
   for(int i=0;i<1;i++)
         {
         output_high(pin_a2);
         delay_us(1000);
         output_low(pin_a2);
         delay_us(19000);
         }
     
}
void set_motor(signed int16 gyro, signed int16 angle2 , int d)
{
   if(gyro>angle2-2 && gyro<angle2+2)
   {
   if(d==1)
   motorspeed(300,300);
   if(d==-1)
   motorspeed(150,150);
   
   }
   else if(angle2>gyro)    
   {
      error=angle2-gyro;
      if(error>=180) 
      {
         error = 360-error;
         if(error>50)
            motorspeed(0,300);
         else
            motorspeed(0,(300-(3*(50-error))));
      }
      else 
      {
         if(error>50)
            motorspeed(300,0);
         else
            motorspeed((300-(3*(50-error))),0);
      }
   }
   else   
   {
      error=gyro-angle2;
      if(error>=180) 
      {
         error = 360-error;
          if(error>50)
            motorspeed(300,0);
         else
            motorspeed((300-(3*(50-error))),0);
      }
      else 
      {
          if(error>50)
            motorspeed(0,300);
         else
            motorspeed(0,(300-(3*(50-error))));
      }
   }
  
}

void main()
{
sg90_open();
motorspeed(0,0);
   LED1_high;
   setup_timer_1(T1_INTERNAL|T1_DIV_BY_1);
   setup_timer_2(T2_DIV_BY_64,255,1);      //f=488hz duty=1023
   
   set_analog_pins(PIN_A1,PIN_A2,PIN_A3,PIN_A5,PIN_E0,PIN_E1,PIN_E2,PIN_B2);
   setup_adc(ADC_CLOCK_DIV_32);
   
   setup_ccp1(CCP_PWM);  //Left Motor
   setup_ccp2(CCP_PWM);  //Right Motor
   set_pwm1_duty((int16)0); //min=0 max=1023
   set_pwm2_duty((int16)0);

   enable_interrupts(INT_TIMER1);
   enable_interrupts(int_rda);
   enable_interrupts(GLOBAL);
   
   for(int j=0;j<3;j++)
   {
      LED1_high;delay_ms(60);LED2_high;delay_ms(60);LED3_high;delay_ms(60);LED4_high;delay_ms(60);
      LED1_low; delay_ms(60);LED2_low; delay_ms(60);LED3_low; delay_ms(60);LED4_low; delay_ms(60);
   }
   if(Lkey)
      {
      LED1_high;
       while(Lkey);
       delay_ms(100);
        Search_i2c(); 
        delay_ms(500);
        i2c_start();  ///Get Offset
        i2c_write(0x24);
        i2c_write(0x01);
        i2c_stop();
        delay_ms(100);
        i2c_start();  //Set Zero
        i2c_write(0x24);
        i2c_write(0x00);
        i2c_stop();
        LED1_low;
      }
   while(TRUE)
   { 
      if(Lkey==0 && cal_done==0) {LED2_high;}
      
      while(Rkey==1 && cal_done==1){ LED1_high;LED4_high;delay_ms(360);LED2_low;LED3_low;delay_ms(360);
                                     LED1_low;LED4_low;delay_ms(360);LED2_high;LED3_high;delay_ms(360); }
      
      while (Rkey==0) {LED1_low; LED2_low;LED3_low;LED4_low;start=1;}
      if(start==1){LED1_high;delay_ms(90);LED1_low;delay_ms(70);LED2_high;delay_ms(90);LED2_low;delay_ms(70);;LED3_high;delay_ms(90);LED3_low;delay_ms(70);}
      //************************************
      
      while(start)
      {
     //Search_i2c();
      //set_gyro_zero();
      //printf("val %Ld \r\n",gyro_value);
      count_sg90_open=0;
      count_sg90_close=0;
      count_sg90_back=0;
      while(TRUE)
      {
      
      
       
     //motorspeed(300,300);    
         set_adc_channel(6);
         delay_us(10);
         float value_adc =read_adc();
         dis=value_adc;
//!         printf("val %f \r\n",value_adc);
//!         delay_ms(200);
         if(angle<=3)angle=4;
         if(angle>=357 && angle<370)angle=356;
         gyro_value=get_gyro_data();
//!         printf("val %Ld \r\n",gyro_value);
//!         delay_ms(200);
         //printf("val %Ld \r\n",gyro_value);.
         if(gyro_value<0)gyro_value=-gyro_value;
         else
         gyro_value=360-gyro_value;
//!        printf("val %Ld \r\n",gyro_value);
//!         delay_ms(200);
         
         //set_motor(gyro_value,90,1);
         
         if(angle==400)
         int u=0;
         else if(angle==600)
         {
            if(dis>=295  && count_sg90_back==0) //256
            {
                  motorspeed(0,0);
                  count_sg90_back=1;
                  sg90_close();
                  char val='g';
                  for(int m=0;m<1;m++) {printf("%c",val);}  
            }
            else
            {
            if(count_sg90_back==1)sg90_close();
            else
            set_motor(gyro_value,gyro_value,1);
            }
            
         }
         else if(angle==500)
         {  
               if(count_sg90_close<1)
               {
                  count_sg90_back=0;
                  motorspeed(0,0);
                  sg90_open();               
               }
               count_sg90_close++;
               if(count_sg90_close==0)count_sg90_close==14;
               if(count_sg90_close>=1 && count_sg90_close<900)  //900
               {
                  motorspeed(-300,-300);                   
               }
               if(count_sg90_close>900)
               {
                  motorspeed(0,0);
                  char val='d';
                  for(int m=0;m<10;m++) {printf("%c",val);} 
               }
         }
         else
         {
            if(count_sg90_back==1)sg90_close();
            count_sg90_close=0;
            set_motor(gyro_value,angle,1);
         }
//!         if(angle==600)dis=value_adc;
//!         else
//!         dis=1;
//!         if((flg_gripper==0) && (dis>=30)){
//!         flg_gripper=1;
//!         motorspeed(0,0);
//!         output_high(pin_a2);
//!         output_high(pin_a3);
//!         delay_ms(1);
//!         output_low(pin_a2);
//!         output_low(pin_a3);
//!         delay_ms(19);
//!         set_motor(gyro_value,gyro_value,1);
//!         delay_ms(500);
//!         motorspeed(0,0);
//!         //l_sg_high;
//!         //r_sg_high;      //open gripper
//!         
//!         
//!         }
//!         else if((flg_gripper==1) && (dis>=30)){
//!         flg_gripper=2;
//!         motorspeed(0,0);
//!         output_high(pin_a3);
//!         output_high(pin_a2);
//!         delay_us(100);
//!         output_low(pin_a3);
//!         delay_us(4900);
//!         output_low(pin_a2);
//!         delay_us(15000);
//!         //l_sg_low;
//!         //r_sg_low;      //close gripper
//!         char val='g';
//!         for(int m=0;m<10;m++) {printf("val %c \r\n",val);}     //get shaft      
//!         }
//!         else if((flg_gripper==2) && (angle!=600)){
//!         set_motor(gyro_value,angle,1);    
//!         flg_gripper=3;
//!         }
//!         else if((flg_gripper==2) && (angle==600)){
//!         motorspeed(0,0);
//!         }
//!         else if(angle==400)motorspeed(0,0);
//!         else if((flg_gripper==3) && (angle==600)){
//!         set_motor(gyro_value,angle,1);
//!         delay_ms(200);
//!         motorspeed(0,0);
//!         output_high(pin_a2);
//!         output_high(pin_a3);
//!         delay_ms(1);
//!         output_low(pin_a2);
//!         output_low(pin_a3);
//!         delay_ms(19);
//!          delay_ms(20);
//!         //l_sg_high;
//!         //r_sg_high;      //open gripper
//!         set_motor(gyro_value,angle,2);
//!         delay_ms(1500);
//!         
//!         for(int m=0;m<10;m++) {printf('g');}     //put shaft 
//!         flg_gripper=0;
//!         }
//!         else{set_motor(gyro_value,angle,1); }

      }
        
         maxspeed=300;
         if(pr>50)
         {
             pr=0;
         }
      }
   }
}

