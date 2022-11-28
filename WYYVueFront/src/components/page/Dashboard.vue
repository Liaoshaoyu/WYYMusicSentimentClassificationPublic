<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="16">
                <el-row :gutter="20" class="mgb20">
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-1">
                                <i class="el-icon-edit-outline grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">
                                        {{ indicator.comments_total }}
                                        <el-tooltip class="item" effect="dark" content="昨日新增评论" placement="right-start"
                                            ><span style="font-size: 14px">(↑{{ indicator.comments_ytd }})</span>
                                        </el-tooltip>
                                    </div>
                                    <div>总评论数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-2">
                                <i class="el-icon-circle-check grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ indicator.has_emotion }}</div>
                                    <div>已做情感分类数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" :body-style="{ padding: '0px' }">
                            <div class="grid-content grid-con-3">
                                <i class="el-icon-s-check grid-con-icon"></i>
                                <div class="grid-cont-right">
                                    <div class="grid-num">{{ indicator.manual }}</div>
                                    <div>手动分类数</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <el-card class="mgb20">
                    <div slot="header" class="clearfix">
                        <span>积极评论Top10歌曲</span>
                    </div>
                    <Charts id="commentsTop10" :option="commentsTop10Option" />
                </el-card>
                <el-card>
                    <div slot="header" class="clearfix">
                        <span>评论长度分布</span>
                    </div>
                    <Charts id="commentsLength" :option="commentsLengthOption" />
                </el-card>
            </el-col>
            <el-col :span="8">
                <el-card class="mgb20">
                    <div slot="header" class="clearfix">
                        <span>评论情感二分类</span>
                    </div>
                    <Charts id="commentsCategory" :option="commentsCategoryOption" />
                </el-card>
                <el-card style="min-height: 500px">
                    <Charts id="wordCloud" :option="wordCloudOption" height="480px" />
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import Charts from '../charts/Charts';
import 'echarts-wordcloud/dist/echarts-wordcloud';
// import "echarts-wordcloud/dist/echarts-wordcloud.min";
import {
    get_song_comments_indicator,
    get_song_comments_category,
    get_song_comments_top10,
    get_song_comments_length,
    get_song_comments_word_cloud
} from '@/api';

export default {
    name: 'dashboard',
    data() {
        return {
            name: localStorage.getItem('ms_username'),
            colors: ['#5470C6', '#91CC75', '#EE6666'],
            commentsCategoryOption: {
                legend: {},
                label: {},
                tooltip: {
                    trigger: 'axis' // axis   item   none三个值
                },
                toolbox: {
                    feature: {
                        dataView: { show: true, readOnly: false },
                        saveAsImage: { show: true }
                    }
                },
                series: [
                    {
                        type: 'pie', //type为pie，表示图表为饼图
                        data: [],
                        label: {
                            normal: {
                                show: true,
                                formatter: '{b}: \n{c}\n({d}%)',
                                position: 'inner'
                            }
                        }
                    }
                ]
            },
            commentsTop10Option: {
                legend: {},
                tooltip: {},
                xAxis: { type: 'category' },
                yAxis: {},
                toolbox: {
                    feature: {
                        dataView: { show: true, readOnly: false },
                        saveAsImage: { show: true }
                    }
                },
                series: [
                    {
                        type: 'bar',
                        name: null,
                        data: [],
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                        barGap: '0%'
                    },
                    {
                        type: 'bar',
                        name: null,
                        data: [],
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        }
                    }
                ]
            },
            commentsLengthOption: {
                color: this.colors,
                tooltip: {
                    // trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                grid: {
                    right: '20%'
                },
                toolbox: {
                    feature: {
                        dataView: { show: true, readOnly: false },
                        saveAsImage: { show: true }
                    }
                },
                legend: {
                    show: false
                    // data: ['Evaporation', 'Temperature']
                },
                xAxis: [
                    {
                        type: 'category',
                        // axisTick: {
                        //     alignWithLabel: true
                        // },
                        // prettier-ignore
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '数量',
                        position: 'right',
                        show: false
                    },
                    {
                        type: 'value',
                        name: '数量',
                        position: 'left',
                        alignTicks: true,
                        axisLine: {
                            show: true
                            // lineStyle: {
                            //     color: '#EE6666'
                            // }
                        }
                    }
                ],
                series: [
                    {
                        name: 'bar',
                        type: 'bar',
                        barGap: '0%',
                        data: []
                    },
                    {
                        name: 'line',
                        type: 'line',
                        yAxisIndex: 1,
                        smooth: true,
                        data: []
                    }
                ]
            },
            wordCloudOption: {
                series: [
                    {
                        type: 'wordCloud',
                        //用来调整词之间的距离
                        gridSize: 10,
                        //用来调整字的大小范围
                        // Text size range which the value in data will be mapped to.
                        // Default to have minimum 12px and maximum 60px size.
                        sizeRange: [14, 60],
                        // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
                        //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
                        // rotationRange: [-45, 0, 45, 90],
                        // rotationRange: [ 0,90],
                        rotationRange: [0, 0],
                        //随机生成字体颜色
                        // maskImage: maskImage,
                        textStyle: {
                            fontFamily: '微软雅黑',
                            color: function () {
                                return (
                                    'rgb(' +
                                    [
                                        Math.round(Math.random() * 250),
                                        Math.round(Math.random() * 250),
                                        Math.round(Math.random() * 250)
                                    ].join(',') +
                                    ')'
                                );
                            }
                        },
                        //位置相关设置
                        // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                        // Default to be put in the center and has 75% x 80% size.
                        left: 'center',
                        top: 'center',
                        right: null,
                        bottom: null,
                        width: '200%',
                        height: '200%',
                        //数据
                        data: []
                    }
                ]
            },
            indicator: {
                comments_total: 0,
                comments_ytd: 0,
                has_emotion: 0,
                manual: 0
            }
        };
    },
    components: {
        Charts
    },
    methods: {
        async initCharts() {
            await get_song_comments_indicator().then((resp) => {
                this.indicator = resp.data;
            });

            await get_song_comments_category().then((resp) => {
                this.commentsCategoryOption.series[0].data = resp.data;
            });

            await get_song_comments_top10().then((resp) => {
                this.commentsTop10Option.series[0].name = '积极评论';
                this.commentsTop10Option.series[0].data = resp.data.positive;

                this.commentsTop10Option.series[1].name = '消极评论';
                this.commentsTop10Option.series[1].data = resp.data.negative;
            });

            await get_song_comments_length().then((resp) => {
                this.commentsLengthOption.xAxis[0].data = resp.data.xaxis;
                this.commentsLengthOption.series[0].data = resp.data.yaxis;
                this.commentsLengthOption.series[1].data = resp.data.yaxis;
            });

            await get_song_comments_word_cloud().then((resp) => {
                this.wordCloudOption.series[0].data = resp.data;
            });
        },
        randomColor() {
            return (
                'rgb(' +
                Math.round(Math.random() * 255) +
                ', ' +
                Math.round(Math.random() * 255) +
                ', ' +
                Math.round(Math.random() * 255) +
                ')'
            );
        }
    },
    created() {
        this.initCharts();
    }
};
</script>


<style scoped>
.el-row {
    margin-bottom: 20px;
}

.grid-content {
    display: flex;
    align-items: center;
    height: 100px;
}

.grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
}

.grid-num {
    font-size: 30px;
    font-weight: bold;
}

.grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
}

.grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
}

.user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
}

.user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}

.user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
}

.user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
}

.user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
}

.user-info-list span {
    margin-left: 70px;
}

.mgb20 {
    margin-bottom: 20px;
}

.el-card is-always-shadow el-card__body {
    margin: 0 10px 10px 0;
}
</style>
