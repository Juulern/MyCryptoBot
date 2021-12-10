import {Fragment} from 'react'
import styled from "styled-components";
import {Button, Icon} from "semantic-ui-react";
import {Pipeline, StartPipeline, StopPipeline} from "../types";


interface Props {
  pipeline: Pipeline
  startPipeline: StartPipeline
  stopPipeline: StopPipeline
}


const Column = styled.div`
    height: 100%;
    width: 50%;
    flex-direction: column;
    justify-content: flex-start;
`


function PipelineButton(props: Props) {

  const {
      startPipeline,
      stopPipeline,
      pipeline,
  } = props

  return (
      <Fragment>
        {pipeline.active ? (
          <Button
            onClick={() => stopPipeline(pipeline.id)}
            style={styles.button}
            color={'red'}
            icon
          >
            <span style={styles.icon}>
              <Icon name={'stop'}/>
            </span>
            Stop Bot
          </Button>
        ) : (
          <Button
              onClick={() => startPipeline(pipeline)}
              style={styles.button}
              color={'green'}
              icon
          >
            <span style={styles.icon}>
              <Icon name={'play'}/>
            </span>
            Start Bot
          </Button>
        )}
      </Fragment>
  );
}

export default PipelineButton;


const styles = {
  button: {
    width: '80%'
  },
  icon: {
    marginRight: '10px'
  }
}