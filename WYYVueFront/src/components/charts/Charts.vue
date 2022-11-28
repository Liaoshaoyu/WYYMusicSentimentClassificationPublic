<template>
    <div :id="id" :style="style"></div>
</template>
  <script>
const echarts = require('echarts');

export default {
    name: 'DualAxisLine',
    data() {
        return {
            //echarts实例
            chart: ''
        };
    },
    props: {
        //父组件需要传递的参数：id，width，height，option
        id: {
            type: String
        },
        width: {
            type: String,
            default: '100%'
        },
        height: {
            type: String,
            default: '300px'
        },
        option: null
    },
    //在Chart.vue中加入watch
    watch: {
        //观察option的变化
        option: {
            handler(newVal, oldVal) {
                if (this.chart) {
                    if (newVal) {
                        this.chart.setOption(newVal);
                    } else {
                        this.chart.setOption(oldVal);
                    }
                } else {
                    this.init();
                }
            },
            deep: true //对象内部属性的监听，关键。
        }
    },
    computed: {
        style() {
            return {
                height: this.height,
                width: this.width,
                display: 'inline-block'
            };
        }
    },
    mounted() {
        this.init();
    },
    methods: {
        init() {
            this.chart = echarts.init(document.getElementById(this.id));
            this.chart.clear();
            this.chart.setOption(this.option);
            window.addEventListener("resize", this.chart.resize);
        }
    }
};
</script>