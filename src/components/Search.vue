<template>
<div class="stickyHeader">
    <div class="headers sticky headerLinks">
        <span class="mainLinkWrapper">
            <a href="https://dfbball.com/" class="mainLink">Home</a>
        </span>
        <span class="mainLinkWrapper">
            <router-link class="mainLink" to="/pick">Pick</router-link>
        </span>
        <span class="mainLinkWrapper">
            <router-link class="mainLink" to="/teams">Teams</router-link>
        </span>
        <span class="mainLinkWrapper">
            <router-link class="mainLink" to="/players">Players</router-link>
        </span>
        <span id="loginButton" v-show="!token" class="mainLinkWrapper">
            <a v-on:click="login()" 
                class="mainLink">Log In</a>
        </span>
        <span id="logoutButton" v-show="token" class="mainLinkWrapper">
            <a v-on:click="logout()" 
                class="mainLink">Log Out</a>
        </span>
    </div>
    <div class="searchWrapper"> 
        <form 
            class="search" 
            @keydown.enter="redirectToPlayerPage"
            v-on:submit.prevent>
            <a href="https://dfbball.com" class="hiddenLink websiteLogoAndName">
                <img class="websiteIcon" src="../assets/ball.png">
                <span class="websiteName">dfbball</span>
            </a>
            <input
                placeholder="search"
                spellcheck="false" 
                class="inpSearch" 
                type="text" 
                v-model="searchInput" 
                >
            <SearchRow
                v-if="this.showPane()" 
                :rowData="searchData[0]"
                v-on:click="redirectToPlayerPage" 
                >
            </SearchRow>
        </form>
    </div>
</div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";
import SearchRow from "@/components/SearchRow.vue"

export default {
    name: "Search",
    components: {
        SearchRow
    },
    data: function() {
        return {
            searchInput: '',
            displayLogout: false
        }
    },
    computed: {
        token() {
            console.log('token',sessionStorage.getItem('token'));
            return sessionStorage.getItem('token');
        },
        searchData() {
            var sitlc = this.searchInput.toLowerCase();
            if (sitlc.length == 0) {
                return [];
            }

            var match = store.state.apiDataTeams.filter(p => (p.city+' '+p.teamName).substring(0, sitlc.length).toLowerCase() == sitlc);
            if (match.length > 0) {
                return match.slice(0, 1).map(function(p) {return {isPlayer: false, id: p.id, name: p.city+' '+p.teamName}});
            }

            match = store.state.apiDataTeams.filter(p => (p.city+' '+p.teamName).toLowerCase().includes(sitlc));

            if (match.length > 0)
            {
                return match.slice(0, 1).map(function(p) {return {isPlayer: false, id: p.id, name: p.city+' '+p.teamName}});
            }
            

            // try to match the full name
            match = store.state.apiDataPlayers.filter(p => (p.firstName+' '+p.lastName).substring(0, sitlc.length).toLowerCase() == sitlc);
            if (match.length > 0) {
                return match.slice(0, 1).map(function(p) {return {isPlayer: true, id: p.id, name: p.firstName+' '+p.lastName}});
            }

            match = store.state.apiDataPlayers.filter(p => (p.firstName+' '+p.lastName).toLowerCase().includes(sitlc));

            return match.slice(0, 1).map(function(p) {return {isPlayer: true, id: p.id, name: p.firstName+' '+p.lastName}});
        },
    },
    methods: {
        fetchPlayers: function() {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/players.php?namesOnly';
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    store.commit('setApiDataPlayers', responseData);
                });
        },
        fetchTeams: function() {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/teams.php';
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    store.commit('setApiDataTeams', responseData);
                });
        },
        logout: function() {
            sessionStorage.removeItem('token');
            console.log('inside logout');
            this.$router.replace({ path: "login" });
            this.displayLogout = false;
            this.$router.go(0);
        },
        login: function() {
            this.$router.replace({ path: "login" });
        },
        getDisplay: function() {
            return sessionStorage.getItem('token');
        },
        redirectToPlayerPage: function() {
            // console.log(this.searchData);
            if (this.searchData.length > 0) {
                router.push('/player/'+this.searchData[0].id)
            }
        },
        showPane: function() {
            return this.searchData.length > 0 && !this.mouseLeft
        }
    },
    created() {
        this.fetchPlayers();
        this.fetchTeams();
    }
}
</script>