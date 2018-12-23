<template>
    <div>
        <p>Player {{ this.obj.firstName }}</p>
        <PlayerCard :playerId="this.obj.id"></PlayerCard>
        <PlayerBoxScore></PlayerBoxScore>
    </div>
</template>

<script>
// @ is an alias to /src
import PlayerBoxScore from "@/components/PlayerBoxScore.vue";
import PlayerCard from "@/components/PlayerCard.vue";
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "Player",
    components: {
        PlayerBoxScore,
        PlayerCard
    },
    computed: {
        obj: function() {
            // console.log(store.state.apiDataPlayers);
            var matchingPlayerArr = store.state.apiDataPlayers.filter(p => p.id == this.$route.params.id);
            if (matchingPlayerArr.length == 0) {
                console.log('no matching player found');
                return {id: -1, firstName: "none", lastName: "none"};
            }
            return matchingPlayerArr[0];
        }
    }
};
</script>