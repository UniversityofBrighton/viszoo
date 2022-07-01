import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode,  } from "react"

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class FamiliaSelector extends StreamlitComponentBase {

  public state = {familias: this.props.args["familias"]}

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.

    const familias = this.state.familias

    const familias_disp = familias.map((fam: { [x: string]: any }, index: number) => {
      if (fam["selected"] === true) {
        return (
        <div>
          <div 
            style={{height:12,width:12,borderRadius:15,backgroundColor:fam["color"],display:"inline-block",}}
            onClick={() => this.onClicked(familias, index)} >
          </div>
          <div style={{display:"inline-block", paddingLeft:10}}>
            {fam["name"]}
          </div>
        </div>
        )
      }
      else {
        return (
          <div>
            <div 
              style={{height:12,width:12,borderRadius:15,backgroundColor:"lightgray",display:"inline-block",}}
              onClick={() => this.onClicked(familias, index)} >
            </div>
            <div style={{display:"inline-block", paddingLeft:10}}>
              {fam["name"]}
            </div>
          </div>
        )
      }
    }

      
    );

    const { theme } = this.props
    var primaryColor = "blue"
    var themeBackgroundColor = "blue"
     if (theme) {
      primaryColor = theme.primaryColor
      themeBackgroundColor = theme.secondaryBackgroundColor
     }

    return (
      <div style={{width:250, margin:0, padding:0,backgroundColor:themeBackgroundColor,borderRadius:12}}>
        <div style={{height:300,overflowY:"scroll",borderRadius:10, paddingLeft:10,}}>
          {familias_disp}
        </div>
        <div style={{
          height:40, backgroundColor: primaryColor,borderRadius:10, paddingTop:10,alignContent:'center',
        }} onClick={() => this.onFilter(familias)}>
          <p style={{paddingLeft:15,fontSize:15,alignContent:'center'}}>filter</p>
        </div>
      </div>
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClicked = (familias: any, index:number) => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    familias[index]["selected"] = !familias[index]["selected"]
    this.setState({familias: familias})
    this.forceUpdate()
  }

  private onFilter = (familias: any) => {
    Streamlit.setComponentValue(familias)
    this.forceUpdate()
  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(FamiliaSelector)
