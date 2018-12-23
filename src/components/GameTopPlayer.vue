<template>
    <div class="game-top-player">
        <img class="playerPhoto" :src="this.imgUrl">
        <div class="game-top-player-stats">
            <div class="player-name">
                {{ this.firstName+" "+this.lastName+" "}}
            </div>
            <div class="player-stat">
                {{ this.player.statpts }}
            </div>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "GameTopPlayer",
    props: {
        gameIndex: {}
    },
    computed: {
        player: function() {
            if (!store.state.apiDataGameTopPlayers[this.$props.gameIndex]) return "";
            return store.state.apiDataGameTopPlayers[this.$props.gameIndex];
        },
        firstName: function() {
            if (!store.state.apiDataGameTopPlayers[this.$props.gameIndex]) return "";
            return store.state.apiDataGameTopPlayers[this.$props.gameIndex].firstName;
        },
        lastName: function() {
            if (!store.state.apiDataGameTopPlayers[this.$props.gameIndex]) return "";
            return store.state.apiDataGameTopPlayers[this.$props.gameIndex].lastName;
        },
        imgUrl: function() {
            if (this.player) return this.player.imgUrl;
            return null;
        },
    },
}
</script>