<template>
    <div class="container">
        <div class="loginContainer">
            <div class="card boxShadow" id="login">
                <h2>Create Account</h2>
                <input class="loginInput" type="text" name="username" @keydown.enter="createAccount" v-model="createInput.username" placeholder="Username" />
                <input class="loginInput" type="password" name="password" @keydown.enter="createAccount" v-model="createInput.password" placeholder="Password" />
                <input class="loginInput" type="password" name="passwordagain" @keydown.enter="createAccount" v-model="createInput.passwordagain" placeholder="Password, again" />
                <span class="errorMessage">{{ this.createErrorMessage }}</span>
                <button class="loginButton" type="button" v-on:click="createAccount()">Create Account and Log In</button>
            </div>
            <div class="card boxShadow" id="login">
                <h2>Existing User</h2>
                <input class="loginInput" type="text" name="username" 
                @keydown.enter="login" v-model="loginInput.username" placeholder="Username" />
                <input class="loginInput" type="password" name="password" @keydown.enter="login" v-model="loginInput.password" placeholder="Password" />
                <span class="errorMessage">{{ this.errorMessage }}</span>
                <button class="loginButton btnLog" type="button" v-on:click="login()">Log In</button>
            </div>
        </div>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: 'Login',
    data() {
        return {
            loginInput: {
                username: "",
                password: ""
            },
            createInput: {
                username: "",
                password: "",
                passwordagain: ""
            },
            errorMessage: "",
            createErrorMessage: "",

        }
    },
    methods: {
        login() {
            if(this.loginInput.username != "" && this.loginInput.password != "") {
                this.sha256(this.loginInput.password).then(result => {
                    this.attemptLogin(this.loginInput.username, result);
                }).catch(error => {
                    this.errorMessage="Something went wrong while trying to log in.";
                });
                
            } else {
                this.errorMessage = "A username and password must be present";
            }
        },
        createAccount() {
            if(this.createInput.username != "" && this.createInput.password != "" && this.createInput.passwordagain != "") {
                if (this.createInput.password != this.createInput.passwordagain) {
                    this.createErrorMessage = "Passwords must match.";
                }
                this.sha256(this.createInput.password).then(result => {
                    this.attemptCreateAccount(this.createInput.username, result);
                }).catch(error => {
                    this.createErrorMessage="Something went wrong while trying to create an account.";
                });
            } else {
                this.createErrorMessage = "All fields must be filled.";
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
        attemptLogin(username, passwordHash) {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/login.php?username='+username+'&passwordHash='+passwordHash;
            console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    if (typeof(responseData.token) !== 'undefined') {
                        sessionStorage.setItem('token', responseData.token);
                        sessionStorage.setItem('username', username);
                        store.commit('setToken', responseData.token);
                        console.log('successful login');
                        vm.errorMessage="";
                        vm.$emit("authenticated", true);
                        vm.$router.replace({ path: "/" });
                        vm.$router.go(0);
                        return;
                    }
                    else {
                        sessionStorage.removeItem('token');
                        sessionStorage.removeItem('username');
                        vm.errorMessage="The username and/or password is incorrect";
                    }
            });
        },
        attemptCreateAccount(username, passwordHash) {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/createLogin.php?username='+username+'&passwordHash='+passwordHash;
            console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    if (responseData.message == 'success') {
                        vm.attemptLogin(username, passwordHash);
                        return;
                    }
                    else {
                        vm.createErrorMessage="Error: "+responseData.message;
                        return;
                    }
            });
        }
    },
    created() {
        if (sessionStorage.getItem('token')) {
            this.$router.replace({ path: "/" });
            this.$router.go(0);
        }
    }
}
</script>