<template>
  <div class="container">
        <MakePicks></MakePicks>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import MakePicks from "@/components/MakePicks.vue";

export default {
  name: "home",
  components: {
    MakePicks
  },
  methods: {
    canChangePicks: function() {
        var res = store.state.apiDataCurrentGames.length > 0 && store.state.apiDataCurrentGames.filter(g => g.playedStatus != 'UNPLAYED').length == 0;
        console.log(res);
        return res;
    },
  },
  created() {
        var hasToken = sessionStorage.getItem('token');
        var canChangePicks = this.canChangePicks();
        // console.log(hasToken, canChangePicks);
        if (!hasToken || !canChangePicks) {
            this.$router.replace({ path: "/" });
            this.$router.go(0);
        }
    }
};
</script>
