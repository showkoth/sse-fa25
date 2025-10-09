import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.*;
import com.ibm.wala.ipa.callgraph.impl.Util;
import com.ibm.wala.ipa.callgraph.propagation.InstanceKey;
import com.ibm.wala.ipa.callgraph.propagation.SSAPropagationCallGraphBuilder;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.config.FileOfClasses;

import java.io.File;
import java.io.FileInputStream;
import java.util.Collection;
import java.util.jar.JarFile;

/**
 * Activity 6 - Static Analysis
 * Implements a 2-CFA call graph for the MusicPlayer.java example.
 *
 * @author Showkoth Hossain
 */

/**
 * To Compile: mvn clean compile
 * To Run: mvn exec:java -Dexec.mainClass="Activity6"
 * Make sure to include the MusicPlayer.jar and JRE libraries in the resources folder.
 * 
 * 
 * I got the following output when I ran the program for 1-CFA call graph:
 * Classes in Application Scope:
  LPlayer
    - Player.play()V
  LDrumPlayer
    - DrumPlayer.<init>()V
    - DrumPlayer.play()V
  LPianoPlayer
    - PianoPlayer.<init>()V
    - PianoPlayer.play()V
  LMusicPlayer
    - MusicPlayer.<init>()V
    - MusicPlayer.main([Ljava/lang/String;)V
  LGuitarPlayer
    - GuitarPlayer.<init>()V
    - GuitarPlayer.play()V

Building 1-CFA Call Graph for MusicPlayer...

=== 1-CFA Call Graph Statistics ===
Call graph stats:
  Nodes: 8464
  Edges: 193635
  Methods: 1542
  Bytecode Bytes: 98546


=== Call Graph (Application Scope) ===
"MusicPlayer.main([Ljava/lang/String;)V" -> "GuitarPlayer.<init>()V"
"MusicPlayer.main([Ljava/lang/String;)V" -> "PianoPlayer.<init>()V"
"MusicPlayer.main([Ljava/lang/String;)V" -> "DrumPlayer.<init>()V"
"MusicPlayer.main([Ljava/lang/String;)V" -> "GuitarPlayer.play()V"
"MusicPlayer.main([Ljava/lang/String;)V" -> "PianoPlayer.play()V"
"MusicPlayer.main([Ljava/lang/String;)V" -> "DrumPlayer.play()V"
"GuitarPlayer.<init>()V" -> "java.lang.Object.<init>()V"
"PianoPlayer.<init>()V" -> "java.lang.Object.<init>()V"
"DrumPlayer.<init>()V" -> "java.lang.Object.<init>()V"
"GuitarPlayer.play()V" -> "java.io.PrintStream.println(Ljava/lang/String;)V"
"PianoPlayer.play()V" -> "java.io.PrintStream.println(Ljava/lang/String;)V"
"DrumPlayer.play()V" -> "java.io.PrintStream.println(Ljava/lang/String;)V"
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  13.866 s
[INFO] Finished at: 2025-10-09T13:02:41-04:00
[INFO] ------------------------------------------------------------------------


But for 2-CFA call graph, the program takes too long to execute and I had to terminate it manually.
 */
public class Activity6 {

    public static void main(String[] args) throws Exception {
        // Create the analysis scope to analyze the MusicPlayer.jar
        AnalysisScope scope = AnalysisScope.createJavaAnalysisScope();
        String path = Activity6.class.getResource("MusicPlayer.jar").getPath();
        scope.addToScope(ClassLoaderReference.Application, new JarFile(new File(path)));
        
        // Add JRE libraries
        String rtPath = Activity6.class.getResource("jdk-17.0.1/rt.jar").getPath();
        scope.addToScope(ClassLoaderReference.Primordial, new JarFile(new File(rtPath)));
        
        // Add exclusions file
        String exPath = Activity6.class.getResource("Java60RegressionExclusions.txt").getPath();
        scope.setExclusions(new FileOfClasses(new FileInputStream(exPath)));

        // Create the class hierarchy
        IClassHierarchy classHierarchy = ClassHierarchyFactory.make(scope);

        // Print the classes in the application scope
        System.out.println("Classes in Application Scope:");
        for (IClass c : classHierarchy) {
            if (c.getClassLoader().getReference().equals(ClassLoaderReference.Application)) {
                System.out.println("  " + c.getName());
                Collection<? extends IMethod> declaredMethods = c.getDeclaredMethods();
                for (IMethod method : declaredMethods) {
                    System.out.println("    - " + method.getSignature());
                }
            }
        }
        System.out.println();

        // Compute entrypoint methods (main methods)
        Iterable<Entrypoint> entrypoints = Util.makeMainEntrypoints(scope, classHierarchy);

        // Create analysis options
        AnalysisOptions options = new AnalysisOptions();
        options.setAnalysisScope(scope);
        options.setEntrypoints(entrypoints);
        AnalysisCache cache = new AnalysisCacheImpl();

        // Create the 2-CFA call graph
        System.out.println("Building 2-CFA Call Graph for MusicPlayer...");
        SSAPropagationCallGraphBuilder twoCfaBuilder = Util.makeNCFABuilder(2, options, cache, classHierarchy, scope);
        CallGraph twoCfaCg = twoCfaBuilder.makeCallGraph(options, null);

        // Print call graph stats
        System.out.println("\n=== 2-CFA Call Graph Statistics ===");
        System.out.println(CallGraphStats.getStats(twoCfaCg));
        System.out.println();

        // Print the call graph (application scope only)
        System.out.println("=== Call Graph (Application Scope) ===");
        for (CGNode n : twoCfaCg) {
            if (n.getMethod().getDeclaringClass().getClassLoader().getReference().equals(ClassLoaderReference.Application)) {
                twoCfaCg.getSuccNodes(n).forEachRemaining(next -> {
                    System.out.println("\"" + n.getMethod().getSignature() + "\" -> \"" + next.getMethod().getSignature() + "\"");
                });
            }
        }
    }
}
