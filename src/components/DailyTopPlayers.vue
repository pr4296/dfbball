<template>
    <div v-if="this.players.length > 0" class="card boxShadow">
        <p class="card-header">{{this.$props.title}}</p>
        <div 
            class="card-row" 
            style="display: flex; 
                align-items: center; 
                flex-direction: row;
                height: 50px;
                border-bottom: none"
            v-for="player in this.players" :key="player.playerId"
            @click="goToPlayer(player.playerId)"
            >
            <img class="card-row-logo" 
                :src="logoUrl(player.abbreviation)">
            <div class="playerName">
                <span 
                    class="card-row-text"
                    style="flex: 1 0 auto"> 
                        <span style="font-size: 1.3em" class="b players-firstName">
                            {{ player.firstName }} 
                        </span>
                        <span style="font-size: 1.3em" class="b players-firstNameInitial">
                            {{ player.firstName != undefined ? player.firstName.substring(0, 1)+"." : ""}} 
                        </span>
                        <span style="font-size: 1.3em" class="b">
                            {{ player.lastName }}
                        </span>
                </span>
            </div>
            <div class="players-fpts" :style="getBgColor(player.fpts, 20)">
                <span class="b">{{ player.fpts }} </span>
                <span class="statLabel">FPTS</span>
            </div>
            <div class="players-pts" :style="getBgColor(player.pts, 10)">
                <span class="b">{{ player.pts }} </span>
                <span class="statLabel">PTS</span>
            </div>
            <div class="players-reb" :style="getBgColor(parseInt(player.offReb)+parseInt(player.defReb), 3)">
                <span class="b" >{{ (parseInt(player.offReb)+parseInt(player.defReb)) }} </span>
                <span class="statLabel">REB</span>
            </div>
            <div class="players-ast" :style="getBgColor(player.ast, 3)">
                <span class="b" >{{ player.ast }} </span>
                <span class="statLabel" >AST</span>
            </div>
            <div class="players-stl" :style="getBgColor(player.stl, 0.6)">
                <span class="b" >{{ player.stl }} </span>
                <span class="statLabel" >STL</span>
            </div>
            <div class="players-blk" :style="getBgColor(player.blk, 0.6)">
                <span class="b">{{ player.blk }} </span>
                <span class="statLabel">BLK</span>
            </div>
            <div class="players-tov" :style="getBgColor(0.4, player.tov*0.2)">
                <span class="b">{{ player.tov }} </span>
                <span class="statLabel">TOV</span>
            </div>
            <div class="players-foulPers" :style="getBgColor(0.4, player.foulPers*0.2)">
                <span class="b">{{ player.foulPers }} </span>
                <span class="statLabel">FLS</span>
            </div>
            <div class="players-plusMinus" :style="getBgColor(parseInt(player.plusMinus)+5, 5)">
                <span class="b">{{ player.plusMinus }} </span>
                <span class="statLabel">PM</span>
            </div>
            <div class="players-mins" :style="getBgColor(player.minSeconds, 60*10)">
                <span class="b">{{ convertToMinSec(player.minSeconds) }} </span>
                <span class="statLabel">MIN</span>
            </div>

        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "DailyTopPlayers",
    props: {
        forGame: {
            type: Number, // game id
            default: 0 // 0 means all teams
        },
        title: {
            default: "Recent Top Players"
        }
    },
    computed: {
        players: function() {
            return store.state.apiDataDailyTopPlayers
        },
        urlParam: function() {
            return this.$props.forGame != 0 ? "?gameId="+this.$props.forGame : "";
        }
    },
    methods: {
        convertToMinSec: function(minSeconds) {
            return Math.floor(minSeconds/60);
        },
        fetchTopPlayers: function() {
            console.log('inside Team fetchTeam', this.$props.forGame);
            var url = 'https://pratyush.rustagi.cc/dfbball/api/todaysTopPlayers.php'+this.urlParam;
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setApiDataDailyTopPlayers', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        getBgColor: function(val, avg) {
            avg = avg*1.01;
            val = val*0.99;
            var r = Math.floor(Math.max(Math.min(126*(val/avg-0.25)+160, 255), 0));
            var g = Math.floor(val/avg > 1 ? Math.max(Math.min((4-val/avg)*75+30, 255), 0) : Math.max(Math.min((4-val/avg)*18+200, 255), 0));
            var b = Math.floor(Math.max(Math.min((4-val/avg)*75+30, 255), 0));
            
            //4x = rgb(255, 30, 30)
            //1x = rgb(255, 255, 255)
            //0.25 = rgb(160, 200, 255)

            var toRet = "border-bottom: 3px solid rgb("+r+", "+g+", "+b+")";
            // if (r > 220 && g < 120) {
                
            //     toRet = "color: #fff; font-weight: 600; "+toRet;
            // }
            //if (val > 35) console.log('toret',r,g);
            return toRet;
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchTopPlayers();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchTopPlayers();
        }
    },
    created() {
        this.fetchTopPlayers();
    }
}
</script>