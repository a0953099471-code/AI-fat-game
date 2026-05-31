import threading
import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

from game import GameEngine, StatsRecorder
from tracker import PoseTracker


st.set_page_config(
    page_title="AI 燃脂闖關遊戲",
    layout="wide"
)

st.title("AI 燃脂闖關遊戲")
st.write(
    "請允許相機存取權限，系統會自動偵測你的動作並將運動轉換成遊戲操作。"
)


# 初始化
if "tracker" not in st.session_state:
    st.session_state.tracker = PoseTracker()

if "stats" not in st.session_state:
    st.session_state.stats = StatsRecorder()

if "game" not in st.session_state:
    st.session_state.game = GameEngine(
        st.session_state.stats
    )

if "lock" not in st.session_state:
    st.session_state.lock = threading.Lock()


class GameVideoTransformer(VideoTransformerBase):

    def transform(self, frame):

        image = frame.to_ndarray(format="bgr24")

        success, encoded = cv2.imencode(
            ".jpg",
            image
        )

        if success:

            label = (
                st.session_state
                .tracker
                .process_image(
                    encoded.tobytes()
                )
            )

            if label:

                with st.session_state.lock:

                    st.session_state.game.handle_action(
                        label
                    )

        return image


def reset_game():

    st.session_state.game = GameEngine(
        st.session_state.stats
    )

    st.session_state.tracker = PoseTracker()



col_left, col_right = st.columns([2, 1])


with col_left:

    st.subheader("即時攝影機偵測")

    webrtc_streamer(
        key="camera",

        video_transformer_factory=
        GameVideoTransformer,

        media_stream_constraints={
            "video": {
                "width": 320,
                "height": 240,
                "frameRate": 10,
            },

            "audio": False,
        },

        async_processing=True,
    )

    st.info(
        "偵測到動作後，遊戲會自動更新。"
    )


with col_right:

    st.subheader("遊戲狀態")

    player = st.session_state.game.player
    boss = st.session_state.game.boss

    latest_record = (
        st.session_state
        .stats
        .latest()
    )

    st.metric(
        "玩家 HP",
        f"{player.hp}/{player.max_hp}"
    )

    st.metric(
        "Boss HP",
        f"{boss.hp}/{boss.max_hp}"
    )

    st.write(
        f"當前動作：{player.last_action}"
    )

    st.write(
        f"BMI：{player.bmi:.1f}"
    )

    st.write(
        f"卡路里：{int(player.calories)}"
    )

    st.write(
        f"運動時間：{int(player.exercise_time)} 秒"
    )

    st.write(
        f"分數：{player.score}"
    )

    st.write(
        f"Boss 等級：{boss.level}"
    )

    if latest_record:

        st.success(
            f"最後紀錄："
            f"{latest_record['date']}"
        )

    else:

        st.write(
            "尚無歷史紀錄"
        )

    if st.button(
        "重新開始遊戲"
    ):

        reset_game()

        st.rerun()


st.write("---")

st.subheader("遊戲說明")

st.markdown("""
- 深蹲 → 攻擊  
- 開合跳 → 集氣  
- 抬腿 → 閃避  
- 平板撐 → 防禦
""")
