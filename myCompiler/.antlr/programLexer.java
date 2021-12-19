// Generated from d:\Compiler\2\myCompiler\program.g4 by ANTLR 4.8
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class programLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		LoE=1, GoE=2, Equal=3, NEqual=4, And=5, Or=6, COMMA=7, SEMI=8, Lb=9, Rb=10, 
		Lsb=11, Rsb=12, Lcb=13, Rcb=14, Lab=15, Rab=16, ASSIGN=17, PLUS=18, MINUS=19, 
		MULTI=20, DIV=21, NOT=22, PERCENT=23, INT=24, VOID=25, IF=26, ELSE=27, 
		WHILE=28, BREAK=29, CONTINUE=30, RETURN=31, CONST=32, Ident=33, Number=34, 
		Decimal_const=35, Octal_const=36, Hexadecimal_const=37, Hexadecimal_prefix=38, 
		Nonzero_digit=39, Octal_digit=40, Hexadecimal_digit=41, Digit=42, Ignore_single=43, 
		Ignore_multi=44, Blank=45;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"LoE", "GoE", "Equal", "NEqual", "And", "Or", "COMMA", "SEMI", "Lb", 
			"Rb", "Lsb", "Rsb", "Lcb", "Rcb", "Lab", "Rab", "ASSIGN", "PLUS", "MINUS", 
			"MULTI", "DIV", "NOT", "PERCENT", "INT", "VOID", "IF", "ELSE", "WHILE", 
			"BREAK", "CONTINUE", "RETURN", "CONST", "Ident", "Number", "Decimal_const", 
			"Octal_const", "Hexadecimal_const", "Hexadecimal_prefix", "Nonzero_digit", 
			"Octal_digit", "Hexadecimal_digit", "Digit", "Ignore_single", "Ignore_multi", 
			"Blank"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'<='", "'>='", "'=='", "'!='", "'&&'", "'||'", "','", "';'", "'('", 
			"')'", "'['", "']'", "'{'", "'}'", "'<'", "'>'", "'='", "'+'", "'-'", 
			"'*'", "'/'", "'!'", "'%'", "'int'", "'void'", "'if'", "'else'", "'while'", 
			"'break'", "'continue'", "'return'", "'const'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "LoE", "GoE", "Equal", "NEqual", "And", "Or", "COMMA", "SEMI", 
			"Lb", "Rb", "Lsb", "Rsb", "Lcb", "Rcb", "Lab", "Rab", "ASSIGN", "PLUS", 
			"MINUS", "MULTI", "DIV", "NOT", "PERCENT", "INT", "VOID", "IF", "ELSE", 
			"WHILE", "BREAK", "CONTINUE", "RETURN", "CONST", "Ident", "Number", "Decimal_const", 
			"Octal_const", "Hexadecimal_const", "Hexadecimal_prefix", "Nonzero_digit", 
			"Octal_digit", "Hexadecimal_digit", "Digit", "Ignore_single", "Ignore_multi", 
			"Blank"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public programLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "program.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2/\u0118\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3"+
		"\6\3\6\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\3\r\3"+
		"\16\3\16\3\17\3\17\3\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3"+
		"\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32\3"+
		"\32\3\32\3\32\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3"+
		"\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3"+
		"\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3\"\3\"\7\""+
		"\u00c7\n\"\f\"\16\"\u00ca\13\"\3#\3#\3#\5#\u00cf\n#\3$\3$\7$\u00d3\n$"+
		"\f$\16$\u00d6\13$\3%\3%\7%\u00da\n%\f%\16%\u00dd\13%\3&\3&\6&\u00e1\n"+
		"&\r&\16&\u00e2\3\'\3\'\3\'\3\'\5\'\u00e9\n\'\3(\3(\3)\3)\3*\5*\u00f0\n"+
		"*\3+\3+\3,\3,\3,\3,\7,\u00f8\n,\f,\16,\u00fb\13,\3,\5,\u00fe\n,\3,\3,"+
		"\3,\3,\3-\3-\3-\3-\7-\u0108\n-\f-\16-\u010b\13-\3-\3-\3-\3-\3-\3.\6.\u0113"+
		"\n.\r.\16.\u0114\3.\3.\4\u00f9\u0109\2/\3\3\5\4\7\5\t\6\13\7\r\b\17\t"+
		"\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27"+
		"-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W"+
		"-Y.[/\3\2\t\5\2C\\aac|\6\2\62;C\\aac|\3\2\63;\3\2\629\5\2\62;CHch\3\2"+
		"\62;\5\2\f\f\17\17\"\"\2\u0122\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t"+
		"\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2"+
		"\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2"+
		"\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2"+
		"+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2"+
		"\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2"+
		"C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3"+
		"\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2"+
		"\2\3]\3\2\2\2\5`\3\2\2\2\7c\3\2\2\2\tf\3\2\2\2\13i\3\2\2\2\rl\3\2\2\2"+
		"\17o\3\2\2\2\21q\3\2\2\2\23s\3\2\2\2\25u\3\2\2\2\27w\3\2\2\2\31y\3\2\2"+
		"\2\33{\3\2\2\2\35}\3\2\2\2\37\177\3\2\2\2!\u0081\3\2\2\2#\u0083\3\2\2"+
		"\2%\u0085\3\2\2\2\'\u0087\3\2\2\2)\u0089\3\2\2\2+\u008b\3\2\2\2-\u008d"+
		"\3\2\2\2/\u008f\3\2\2\2\61\u0091\3\2\2\2\63\u0095\3\2\2\2\65\u009a\3\2"+
		"\2\2\67\u009d\3\2\2\29\u00a2\3\2\2\2;\u00a8\3\2\2\2=\u00ae\3\2\2\2?\u00b7"+
		"\3\2\2\2A\u00be\3\2\2\2C\u00c4\3\2\2\2E\u00ce\3\2\2\2G\u00d0\3\2\2\2I"+
		"\u00d7\3\2\2\2K\u00de\3\2\2\2M\u00e8\3\2\2\2O\u00ea\3\2\2\2Q\u00ec\3\2"+
		"\2\2S\u00ef\3\2\2\2U\u00f1\3\2\2\2W\u00f3\3\2\2\2Y\u0103\3\2\2\2[\u0112"+
		"\3\2\2\2]^\7>\2\2^_\7?\2\2_\4\3\2\2\2`a\7@\2\2ab\7?\2\2b\6\3\2\2\2cd\7"+
		"?\2\2de\7?\2\2e\b\3\2\2\2fg\7#\2\2gh\7?\2\2h\n\3\2\2\2ij\7(\2\2jk\7(\2"+
		"\2k\f\3\2\2\2lm\7~\2\2mn\7~\2\2n\16\3\2\2\2op\7.\2\2p\20\3\2\2\2qr\7="+
		"\2\2r\22\3\2\2\2st\7*\2\2t\24\3\2\2\2uv\7+\2\2v\26\3\2\2\2wx\7]\2\2x\30"+
		"\3\2\2\2yz\7_\2\2z\32\3\2\2\2{|\7}\2\2|\34\3\2\2\2}~\7\177\2\2~\36\3\2"+
		"\2\2\177\u0080\7>\2\2\u0080 \3\2\2\2\u0081\u0082\7@\2\2\u0082\"\3\2\2"+
		"\2\u0083\u0084\7?\2\2\u0084$\3\2\2\2\u0085\u0086\7-\2\2\u0086&\3\2\2\2"+
		"\u0087\u0088\7/\2\2\u0088(\3\2\2\2\u0089\u008a\7,\2\2\u008a*\3\2\2\2\u008b"+
		"\u008c\7\61\2\2\u008c,\3\2\2\2\u008d\u008e\7#\2\2\u008e.\3\2\2\2\u008f"+
		"\u0090\7\'\2\2\u0090\60\3\2\2\2\u0091\u0092\7k\2\2\u0092\u0093\7p\2\2"+
		"\u0093\u0094\7v\2\2\u0094\62\3\2\2\2\u0095\u0096\7x\2\2\u0096\u0097\7"+
		"q\2\2\u0097\u0098\7k\2\2\u0098\u0099\7f\2\2\u0099\64\3\2\2\2\u009a\u009b"+
		"\7k\2\2\u009b\u009c\7h\2\2\u009c\66\3\2\2\2\u009d\u009e\7g\2\2\u009e\u009f"+
		"\7n\2\2\u009f\u00a0\7u\2\2\u00a0\u00a1\7g\2\2\u00a18\3\2\2\2\u00a2\u00a3"+
		"\7y\2\2\u00a3\u00a4\7j\2\2\u00a4\u00a5\7k\2\2\u00a5\u00a6\7n\2\2\u00a6"+
		"\u00a7\7g\2\2\u00a7:\3\2\2\2\u00a8\u00a9\7d\2\2\u00a9\u00aa\7t\2\2\u00aa"+
		"\u00ab\7g\2\2\u00ab\u00ac\7c\2\2\u00ac\u00ad\7m\2\2\u00ad<\3\2\2\2\u00ae"+
		"\u00af\7e\2\2\u00af\u00b0\7q\2\2\u00b0\u00b1\7p\2\2\u00b1\u00b2\7v\2\2"+
		"\u00b2\u00b3\7k\2\2\u00b3\u00b4\7p\2\2\u00b4\u00b5\7w\2\2\u00b5\u00b6"+
		"\7g\2\2\u00b6>\3\2\2\2\u00b7\u00b8\7t\2\2\u00b8\u00b9\7g\2\2\u00b9\u00ba"+
		"\7v\2\2\u00ba\u00bb\7w\2\2\u00bb\u00bc\7t\2\2\u00bc\u00bd\7p\2\2\u00bd"+
		"@\3\2\2\2\u00be\u00bf\7e\2\2\u00bf\u00c0\7q\2\2\u00c0\u00c1\7p\2\2\u00c1"+
		"\u00c2\7u\2\2\u00c2\u00c3\7v\2\2\u00c3B\3\2\2\2\u00c4\u00c8\t\2\2\2\u00c5"+
		"\u00c7\t\3\2\2\u00c6\u00c5\3\2\2\2\u00c7\u00ca\3\2\2\2\u00c8\u00c6\3\2"+
		"\2\2\u00c8\u00c9\3\2\2\2\u00c9D\3\2\2\2\u00ca\u00c8\3\2\2\2\u00cb\u00cf"+
		"\5G$\2\u00cc\u00cf\5I%\2\u00cd\u00cf\5K&\2\u00ce\u00cb\3\2\2\2\u00ce\u00cc"+
		"\3\2\2\2\u00ce\u00cd\3\2\2\2\u00cfF\3\2\2\2\u00d0\u00d4\5O(\2\u00d1\u00d3"+
		"\5U+\2\u00d2\u00d1\3\2\2\2\u00d3\u00d6\3\2\2\2\u00d4\u00d2\3\2\2\2\u00d4"+
		"\u00d5\3\2\2\2\u00d5H\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d7\u00db\7\62\2\2"+
		"\u00d8\u00da\5Q)\2\u00d9\u00d8\3\2\2\2\u00da\u00dd\3\2\2\2\u00db\u00d9"+
		"\3\2\2\2\u00db\u00dc\3\2\2\2\u00dcJ\3\2\2\2\u00dd\u00db\3\2\2\2\u00de"+
		"\u00e0\5M\'\2\u00df\u00e1\5S*\2\u00e0\u00df\3\2\2\2\u00e1\u00e2\3\2\2"+
		"\2\u00e2\u00e0\3\2\2\2\u00e2\u00e3\3\2\2\2\u00e3L\3\2\2\2\u00e4\u00e5"+
		"\7\62\2\2\u00e5\u00e9\7z\2\2\u00e6\u00e7\7\62\2\2\u00e7\u00e9\7Z\2\2\u00e8"+
		"\u00e4\3\2\2\2\u00e8\u00e6\3\2\2\2\u00e9N\3\2\2\2\u00ea\u00eb\t\4\2\2"+
		"\u00ebP\3\2\2\2\u00ec\u00ed\t\5\2\2\u00edR\3\2\2\2\u00ee\u00f0\t\6\2\2"+
		"\u00ef\u00ee\3\2\2\2\u00f0T\3\2\2\2\u00f1\u00f2\t\7\2\2\u00f2V\3\2\2\2"+
		"\u00f3\u00f4\7\61\2\2\u00f4\u00f5\7\61\2\2\u00f5\u00f9\3\2\2\2\u00f6\u00f8"+
		"\13\2\2\2\u00f7\u00f6\3\2\2\2\u00f8\u00fb\3\2\2\2\u00f9\u00fa\3\2\2\2"+
		"\u00f9\u00f7\3\2\2\2\u00fa\u00fd\3\2\2\2\u00fb\u00f9\3\2\2\2\u00fc\u00fe"+
		"\7\17\2\2\u00fd\u00fc\3\2\2\2\u00fd\u00fe\3\2\2\2\u00fe\u00ff\3\2\2\2"+
		"\u00ff\u0100\7\f\2\2\u0100\u0101\3\2\2\2\u0101\u0102\b,\2\2\u0102X\3\2"+
		"\2\2\u0103\u0104\7\61\2\2\u0104\u0105\7,\2\2\u0105\u0109\3\2\2\2\u0106"+
		"\u0108\13\2\2\2\u0107\u0106\3\2\2\2\u0108\u010b\3\2\2\2\u0109\u010a\3"+
		"\2\2\2\u0109\u0107\3\2\2\2\u010a\u010c\3\2\2\2\u010b\u0109\3\2\2\2\u010c"+
		"\u010d\7,\2\2\u010d\u010e\7\61\2\2\u010e\u010f\3\2\2\2\u010f\u0110\b-"+
		"\2\2\u0110Z\3\2\2\2\u0111\u0113\t\b\2\2\u0112\u0111\3\2\2\2\u0113\u0114"+
		"\3\2\2\2\u0114\u0112\3\2\2\2\u0114\u0115\3\2\2\2\u0115\u0116\3\2\2\2\u0116"+
		"\u0117\b.\2\2\u0117\\\3\2\2\2\16\2\u00c8\u00ce\u00d4\u00db\u00e2\u00e8"+
		"\u00ef\u00f9\u00fd\u0109\u0114\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}