 function validate(){

      var name=document.getElementById("nn");
      var last=document.getElementById("ll");
      var email=document.getElementById("ee");
      var phone=document.getElementById("pp");
      var dob=document.getElementById("dd");
      var address=document.getElementById("aa");


      if(name.value.trim()==""){
      alert("Name field can not be empty !!!");
      return false;
      }
      else if(last.value.trim()=""){
       alert("Last Name field can not be empty !!!");
      return false;
      }
      else if(email.value.trim()=""){
       alert("email field can not be empty !!!");
      return false;
      }else if(dob.value.trim()=""){
       alert("Dob field can not be empty !!!");
      return false;
      }else if(Phone.value.trim()=""){
       alert("Phone number field can not be empty !!!");
      return false;
      }else if(address.value.trim()=""){
       alert("Address field can not be empty !!!");
      return false;
      }
      else{
      true;
      }




      }
