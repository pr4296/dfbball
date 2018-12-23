<template>
<div class="card boxShadow">
    <p class="card-header">Upcoming Games</p>
    <div class="card-row" 
        v-for="game in this.games" :key="game.id"
        @click="goToGame(game.id)"
        >

        <img 
            class="card-row-logo" 
            :src="logoUrl(game.awayTeamAbbreviation)"> 

        <span class="card-row-text">vs</span>

        <img 
            class="card-row-logo" 
            :src="logoUrl(game.homeTeamAbbreviation)">

        <span 
            class="card-row-text"> 
                {{ getLocalGameTime(game.startTime) }}
        </span>
    </div>
</div>
</template>


<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "Search",
    computed: {
        games: function() {
            return store.state.apiDataUpcomingGames
        }
    },
    methods: {
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        getLocalGameTime: function(date) {
            var utcDatePlusOffset = new Date(date);
            var offset = utcDatePlusOffset.getTimezoneOffset();
            var gameDateFull = new Date(utcDatePlusOffset-offset*60*1000);

            var currDate = new Date();
            var gameDate = new Date(gameDateFull.getFullYear(), gameDateFull.getMonth(), gameDateFull.getDate());
            var gameTime = gameDateFull.toLocaleTimeString();
            gameTime = gameTime.substring(0, gameTime.length-6)+" "+gameTime.substring(gameTime.length-2, gameTime.length);  
            
            console.log(gameDate, currDate);

            if (currDate.toDateString().substring(0, 14) == gameDateFull.toDateString().substring(0, 14)) {
                return "Today "+gameTime;
            }
            else {
                
            }
            if (currDate - gameDate < 24*60*60*1000 && currDate > gameDate) return "Yesterday "+gameTime;
            if (currDate - gameDate > -24*60*60*1000 && currDate < gameDate) return "Tomorrow "+gameTime;
            // console.log('at end');

            var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

            
            gameDate = days[gameDate.getDay()]+", "+months[gameDate.getMonth()]+" "+gameDate.getDate()+" "+gameTime;
            return gameDate;
        },
        fetchUpcomingGames: function() {
            console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/basketbrief/api/upcomingGames.php?id='+this.$route.params.id;
            console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    // console.log(responseData);
                    store.commit('setApiDataUpcomingGames', responseData);
            });
        },
        goToGame: function(gameId) {
            router.push('/game/'+gameId)
        },
        goToTeam: function(teamId) {
            router.push('/team/'+teamId)
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchUpcomingGames();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchUpcomingGames();
        }
    },
    created() {
        this.fetchUpcomingGames();
    }
}
</script>