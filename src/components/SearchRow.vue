<template>
    <div 
        @click="goToPage(rowData.id)">
        <button class="btnSearch">
            {{ rowData.name }}
        </button>
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "SearchRow",
    props: ['rowData'],
    computed: {
        itemPath: function() {
            return this.rowData.isPlayer ? '/player/'+this.rowData.id : '/team/'+this.rowData.id;
        }
    },
    methods: {
        goToPage : function(id) {
            router.push(this.itemPath)
        }
    }
}
</script>
