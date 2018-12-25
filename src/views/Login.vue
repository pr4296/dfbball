<template>
    <div class="card boxShadow" id="login">
        <h2>Existing User</h2>
        <input class="loginInput" type="text" name="username" v-model="input.username" placeholder="Username" />
        <input class="loginInput" type="password" name="password" v-model="input.password" placeholder="Password" />
        <span class="errorMessage">{{ this.errorMessage }}</span>
        <button class="loginButton" type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: 'Login',
    data() {
        return {
            input: {
                username: "",
                password: ""
            },
            errorMessage: "",
        }
    },
    methods: {
        login() {
            if(this.input.username != "" && this.input.password != "") {
                this.sha256(this.input.password).then(result => {
                    if (this.attemptLogin(this.input.username, result)) {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "userpage" });
                    } else {
                        this.errorMessage="The username and / or password is incorrect";
                    }
                }).catch(error => {
                    this.errorMessage="Something went wrong while trying to log in.";
                });
                
            } else {
                this.errorMessage = "A username and password must be present";
            }
        },
        async sha256(message) {
            // encode as UTF-8
            const msgBuffer = new TextEncoder('utf-8').encode(message);     
            // hash the message
            const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
            // convert ArrayBuffer to Array
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            // convert bytes to hex string                  
            const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
            return hashHex;
        },
        attemptLogin: function(username, passwordHash) {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/login.php?username='+username+'&passwordHash='+passwordHash;
            console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    if (typeof(responseData.token) !== 'undefined') {
                        store.commit('setToken', responseData.token);
                        console.log('successful login');
                        return true;
                    }
                    console.log('failed login', responseData);
                    return false;
            });
        },
    }
}
</script>