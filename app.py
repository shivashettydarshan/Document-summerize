import streamlit as st
import os
import tempfile
from io import BytesIO
from document_processor import DocumentProcessor
from ai_summarizer import AISummarizer
from utils import format_file_size, validate_file_type

# Configure page
st.set_page_config(
    page_title="Legal Document Summarizer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize processors
@st.cache_resource
def get_processors():
    doc_processor = DocumentProcessor()
    ai_summarizer = AISummarizer()
    return doc_processor, ai_summarizer

def main():
    st.title("⚖️ Legal Document Summarizer")
    st.markdown("AI-powered legal document analysis and summarization tool")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # AI Provider selection
        ai_provider = st.selectbox(
            "Select AI Provider",
            ["OpenAI", "Anthropic"],
            help="Choose your preferred AI service for document summarization"
        )
        
        # Summary length
        summary_length = st.selectbox(
            "Summary Length",
            ["Brief", "Standard", "Detailed"],
            index=1,
            help="Choose the desired length of the summary"
        )
        
        # Focus areas
        st.subheader("Focus Areas")
        focus_areas = []
        if st.checkbox("Key Legal Points", value=True):
            focus_areas.append("key legal points")
        if st.checkbox("Obligations & Rights"):
            focus_areas.append("obligations and rights")
        if st.checkbox("Dates & Deadlines"):
            focus_areas.append("important dates and deadlines")
        if st.checkbox("Financial Terms"):
            focus_areas.append("financial terms and amounts")
        if st.checkbox("Risk Factors"):
            focus_areas.append("risk factors")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Document Upload")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload your legal document",
            type=["pdf", "txt", "docx"],
            help="Supported formats: PDF, TXT, DOCX (Max size: 200MB)"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {format_file_size(uploaded_file.size)}")
            
            # Validate file type
            if not validate_file_type(uploaded_file.name):
                st.error("❌ Unsupported file type. Please upload PDF, TXT, or DOCX files only.")
                return
            
            # Process document button
            if st.button("🔍 Analyze Document", type="primary"):
                try:
                    doc_processor, ai_summarizer = get_processors()
                    
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Extract text
                    status_text.text("📖 Extracting text from document...")
                    progress_bar.progress(25)
                    
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        # Extract text
                        extracted_text = doc_processor.extract_text(tmp_file_path, uploaded_file.name)
                        
                        if not extracted_text.strip():
                            st.error("❌ No text could be extracted from the document. Please ensure the document contains readable text.")
                            return
                        
                        progress_bar.progress(50)
                        
                        # Step 2: Generate summary
                        status_text.text("🤖 Generating AI summary...")
                        progress_bar.progress(75)
                        
                        # Create summary prompt based on focus areas
                        focus_text = ", ".join(focus_areas) if focus_areas else "general legal analysis"
                        
                        summary = ai_summarizer.summarize_document(
                            text=extracted_text,
                            provider=ai_provider.lower(),
                            length=summary_length.lower(),
                            focus_areas=focus_text
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
                        # Store results in session state
                        st.session_state['original_text'] = extracted_text
                        st.session_state['summary'] = summary
                        st.session_state['document_name'] = uploaded_file.name
                        
                    finally:
                        # Clean up temporary file
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
                        
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()
    
    with col2:
        st.header("📋 Document Summary")
        
        # Display summary if available
        if 'summary' in st.session_state:
            st.success("✅ Summary generated successfully!")
            
            # Summary content
            st.subheader("AI-Generated Summary")
            st.markdown(st.session_state['summary'])
            
            # Download summary
            summary_bytes = st.session_state['summary'].encode('utf-8')
            st.download_button(
                label="📥 Download Summary",
                data=summary_bytes,
                file_name=f"summary_{st.session_state['document_name'].rsplit('.', 1)[0]}.txt",
                mime="text/plain"
            )
            
            # Word count info
            summary_words = len(st.session_state['summary'].split())
            original_words = len(st.session_state['original_text'].split())
            compression_ratio = (1 - summary_words / original_words) * 100 if original_words > 0 else 0
            
            st.info(f"📊 Summary: {summary_words:,} words | Original: {original_words:,} words | Compression: {compression_ratio:.1f}%")
        else:
            st.info("👆 Upload a document and click 'Analyze Document' to generate a summary.")
    
    # Original document viewer (expandable)
    if 'original_text' in st.session_state:
        with st.expander("📖 View Original Document Text", expanded=False):
            st.text_area(
                "Original Document Content",
                value=st.session_state['original_text'],
                height=400,
                disabled=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <small>⚖️ Legal Document Summarizer | Powered by AI | For legal professionals</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
